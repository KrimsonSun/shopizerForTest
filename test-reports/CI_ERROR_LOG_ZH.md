# CI 作业错误记录（中文）

> 记录日期：2026-02-18  
> 目的：按步骤记录构建/测试过程中出现的错误，便于作业提交时展示“过程 + 问题 + 处理”。

## 记录规范
- 每执行一个关键步骤（如：安装、构建、测试、推送、触发 CI），新增一条记录。
- 如果命令成功，也建议记录为“成功（无错误）”。
- 报错优先记录：命令、退出码、核心错误摘要、初步原因、下一步处理。

## 错误记录（按时间顺序）

### 步骤 1：使用 VS Code 测试工具运行单测
- **动作**：运行 `ProductPricePartitionTest.java`
- **结果**：未得到可执行的 Java 测试统计（显示 `passed=0 failed=0`）
- **错误/现象**：测试工具未返回实际 JUnit 执行结果
- **初步判断**：该工具在当前项目结构下未正确识别 Maven/JUnit 测试运行
- **下一步处理**：改用 Maven 命令直接执行测试（与 CI 一致）

### 步骤 2：运行 sm-core 定向测试
- **命令**：`./mvnw -pl sm-core -Dtest=ProductPricePartitionTest test`
- **退出码**：`1`
- **结果**：`BUILD FAILURE`
- **核心错误摘要**：
  - `Tests run: 21, Failures: 5, Errors: 0, Skipped: 0`
  - 失败用例包括：
    - `testPartition5_InvalidNegativePrice`
    - `testPartition5_BoundaryNegative_JustBelowZero`
    - `testPartition6_InvalidDecimalPrecision_ThreeDecimals`
    - `testPartition6_InvalidDecimalPrecision_ExtremeDecimals`
    - `testPartition7_InvalidNullPrice_HandlesGracefully`
- **附加日志现象**：启动期间出现 `CacheManagerImpl` 的 `NullPointerException` 日志
- **初步判断**：当前测试类存在预期失败（用于暴露缺陷），不适合作为“CI 必须通过”的默认门禁测试
- **下一步处理**：将该类作为“缺陷复现”证据保留；为 CI 主流程选择可稳定通过的测试集或先修复业务逻辑

### 步骤 3：运行 sm-shop 定向测试
- **命令**：`./mvnw -pl sm-shop -Dtest=GeneratePasswordTest test`
- **退出码**：`1`
- **结果**：`BUILD FAILURE`
- **核心错误摘要**：
  - `Could not resolve dependencies`
  - `Failed to collect dependencies at com.shopizer:sm-core:jar:3.2.5`
  - `Could not transfer artifact ... from/to spring-releases ... : Not authorized`
- **初步判断**：
  - Maven 在拉取 `com.shopizer:sm-core:3.2.5` 时走到远程仓库 `spring-releases`，并被拒绝授权；
  - 本地 reactor 产物未被正确复用（或未先完成本地安装），导致依赖解析失败。
- **下一步处理（建议）**：
  - 先在仓库根目录执行多模块构建：`./mvnw -DskipTests install`（先装本地依赖），再跑目标测试；
  - 或使用 `-am` 让 Maven 自动构建依赖模块：`./mvnw -pl sm-shop -am test`。

### 步骤 4：验证 sm-core-model 模块构建
- **命令**：`./mvnw -pl sm-core-model test`
- **退出码**：`0`
- **结果**：`BUILD SUCCESS`
- **执行摘要**：`No tests to run.`
- **说明**：该模块可作为“构建成功”证明，但不能单独证明“测试用例已执行”。

### 步骤 5：验证 sm-core 可执行测试（DataUtils）
- **命令**：`./mvnw -pl sm-core -Dtest=DataUtilsTest test`
- **退出码**：`0`
- **结果**：`BUILD SUCCESS`
- **执行摘要**：`Tests run: 9, Failures: 0, Errors: 0, Skipped: 0`
- **附加现象**：日志出现 JaCoCo 对 JDK 高版本类的 instrumentation 警告（`Unsupported class file major version 69`），但未导致构建失败。
- **结论**：该命令适合作为当前 CI 作业的“可稳定通过且确实执行测试”的基线。

### 步骤 6：验证另一测试目标（ShippingMethodDecisionTest）
- **命令**：`./mvnw -pl sm-core -Dtest=ShippingMethodDecisionTest test`
- **退出码**：`0`
- **结果**：`BUILD SUCCESS`
- **执行摘要**：`Tests run: 1, Failures: 0, Errors: 0, Skipped: 1`
- **说明**：该测试被跳过（Skipped），不适合作为“已执行测试用例”的主证明。

### 步骤 7：本地复现 CI 命令（首次失败）
- **命令**：`./mvnw -B -ntp -pl sm-core -Dtest=DataUtilsTest test`
- **退出码**：`1`
- **结果**：`BUILD FAILURE`
- **核心错误摘要**：`Unable to parse command line options: Unrecognized option: -ntp`
- **初步判断**：项目 Maven Wrapper 版本为 3.5.2，不支持 `-ntp` 参数。
- **下一步处理**：从 CI 命令中移除 `-ntp`。

### 步骤 8：修正 CI 命令后复测
- **命令**：`./mvnw -B -pl sm-core -Dtest=DataUtilsTest test`
- **退出码**：`0`
- **结果**：`BUILD SUCCESS`
- **执行摘要**：`Tests run: 9, Failures: 0, Errors: 0, Skipped: 0`
- **结论**：修正后的命令可用于 GitHub Actions 工作流。

### 步骤 9：新增 CI 配置文件
- **文件**：`.github/workflows/ci.yml`
- **关键行为**：`checkout` + `setup-java(17)` + `./mvnw -B -pl sm-core -Dtest=DataUtilsTest test`
- **状态**：已创建，可提交后触发 GitHub Actions。

### 步骤 10：GitHub Actions 首次 web 运行失败（依赖解析）
- **现象**：CI 日志报错 `Could not resolve dependencies ... com.shopizer:sm-core-model ... from/to spring-releases ... Not authorized`
- **根因**：workflow 只构建了 `sm-core`，未在同一 reactor 中先构建其本地依赖模块，Maven 转而访问远程仓库拉取 `sm-core-model`，被仓库权限拒绝。
- **修复**：将命令改为 `./mvnw -B -pl sm-core -am -Dtest=DataUtilsTest test`，使用 `-am` 自动构建依赖模块。
- **提交建议**：提交该修复后重新触发 Actions，并截图保留“失败一次 + 修复后通过”的证据。

### 步骤 11：GitHub Actions 二次失败（No tests were executed）
- **现象**：CI 报错 `Failed to execute goal ... maven-surefire-plugin ... on project sm-core-model: No tests were executed!`
- **根因**：使用 `-am` 后会进入 `sm-core-model` 等依赖模块；但 `-Dtest=DataUtilsTest` 仅在 `sm-core` 有匹配测试，其他模块无匹配时 surefire 按默认策略失败。
- **修复**：将命令改为 `./mvnw -B -pl sm-core -am -Dtest=DataUtilsTest -DfailIfNoTests=false test`。
- **本地验证**：Reactor Summary 显示 `shopizer / sm-core-model / sm-core-modules / sm-core` 全部 `SUCCESS`，并且 `DataUtilsTest` 执行结果为 `Tests run: 9, Failures: 0, Errors: 0, Skipped: 0`。

---

## 作业提交时可引用的“问题说明”模板
- **问题**：命令/步骤名称
- **现象**：关键报错 + 截图
- **原因分析**：依赖、环境、测试数据、代码缺陷等
- **解决方案**：已尝试操作 + 最终修复方案
- **结果**：已解决 / 暂未解决（附后续计划）

## 待补充（你后续执行时继续追加）
- GitHub Actions workflow 触发截图
- CI 页面中的 `build`、`test` job 日志截图
- 修复后重新运行并通过的截图
