# Shopizer 测试文档索引
## Complete Testing Documentation Index

**更新时间**: 2026年2月7日  
**项目**: Shopizer E-commerce Platform  
**课程**: 软件测试 - 第二次作业指导

---

## 🎯 快速导航

### 如果你想要...

| 你想要 | 看这些文档 | 优先级 |
|------|---------|-------|
| **了解功能划分** | 1️⃣ [WORK_DIVISION_SUMMARY.md](#) (本索引) → 2️⃣ [FEATURE_DIVISION_ANALYSIS.md](#) | ⭐⭐⭐ |
| **规划第二次作业** | 1️⃣ [WORK_DIVISION_SUMMARY.md](#) → 2️⃣ [PRODUCT_LISTING_FSM_DESIGN.md](#) | ⭐⭐⭐⭐⭐ |
| **学习我的价格测试** | [PRODUCT_PRICE_TEST_REPORT_EN.md](#) 或 [PRODUCT_PRICE_TEST_REPORT_ZH.md](#) | ⭐⭐⭐ |
| **学习购物车测试** | [TEST_ENHANCEMENT_SUMMARY.md](#) | ⭐⭐⭐ |
| **查看现有测试代码** | [sm-shop/src/test/java](#) | ⭐⭐ |
| **理解项目结构** | [PROJECT_TEST_REPORT.md](#) | ⭐⭐ |
| **配置测试环境** | [TEST_ENVIRONMENT_SETUP.md](#) | ⭐⭐ (首次只需看一次) |
| **学习测试最佳实践** | [TESTING_GUIDE.md](#) | ⭐⭐⭐ |

---

## 📑 完整文档清单

### 【第二次作业相关】🆕 新增文档

#### 1. [WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md) ⭐⭐⭐⭐⭐
**内容**: 你与朋友的功能测试分工  
**用途**: 快速了解功能划分,避免冲突  
**适合人群**: 你和朋友一起读  
**关键部分**:
- 核心问题回答 (会不会冲突?)
- 职责分工对比表
- 冲突风险矩阵
- 推荐的作业题目设计
- 冲突检查清单

**建议阅读时间**: 15分钟  
**行动项**: 
- [ ] 与朋友讨论分工方案
- [ ] 确认订单价格验证的界线

---

#### 2. [FEATURE_DIVISION_ANALYSIS.md](FEATURE_DIVISION_ANALYSIS.md) ⭐⭐⭐⭐
**内容**: 详细的功能划分与冲突分析报告  
**用途**: 深入理解为什么这样划分,冲突如何产生  
**适合人群**: 需要理论背景的人  
**关键部分**:
- 架构概览 (Shopizer整体结构)
- 现有功能划分详解
- 冲突点分析 (3个潜在冲突)
- 建议的划分方案 (3个方案对比)
- 有限状态机建议

**建议阅读时间**: 30分钟  
**行动项**: 
- [ ] 理解架构
- [ ] 选择推荐方案A

---

#### 3. [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md) ⭐⭐⭐⭐⭐
**内容**: 产品上架流程的完整FSM设计(你的第二次作业建议)  
**用途**: 为你的第二次作业提供详细框架  
**适合人群**: 你的主要参考资料  
**关键部分**:
- 为什么选择产品上架作为FSM
- FSM的概念简述
- 7个核心状态的详细解析
- 状态转换表和守卫条件
- 价格在FSM中的角色
- 31个完整的JUnit测试用例框架
- 与Shopizer实际代码的映射

**建议阅读时间**: 45分钟 (第一遍) + 30分钟 (实现)  
**行动项**: 
- [ ] 理解产品生命周期的7个状态
- [ ] 学习如何将价格分区测试集成到FSM中
- [ ] 规划31个测试用例的实现

---

### 【第一次作业成果】✅ 已完成的工作

#### 4. [PRODUCT_PRICE_TEST_REPORT_EN.md](PRODUCT_PRICE_TEST_REPORT_EN.md) ⭐⭐⭐
**内容**: 产品价格分区测试详细报告(英文版)  
**用途**: 你现有的价格测试成果展示  
**适合人群**: 课程评审、同学参考  
**关键部分**:
- 测试概览(目标、范围、环境)
- 测试策略(分区、边界值)
- 详细测试用例(P1-P7)
- 测试结果汇总
- 测试覆盖率分析
- 发现的问题和建议

**包含内容**: 约800行,非常详细  
**测试用例数**: 14个核心分区和边界值测试  

**建议阅读时间**: 20分钟 (浏览) / 45分钟 (详读)  
**重点关注**:
- 7个分区的定义和代表值
- 8个关键边界值
- 发现的bugs

---

#### 5. [PRODUCT_PRICE_TEST_REPORT_ZH.md](PRODUCT_PRICE_TEST_REPORT_ZH.md) ⭐⭐⭐
**内容**: 产品价格分区测试详细报告(中文版)  
**用途**: 中文语境下的详细解释  
**适合人群**: 偏好中文的人  

**与英文版本的关系**: 大致相同内容,中文编写  

---

#### 6. [TEST_ENHANCEMENT_SUMMARY.md](TEST_ENHANCEMENT_SUMMARY.md) ⭐⭐⭐
**内容**: MyCartQuantityTest 扩展测试用例说明  
**用途**: 购物车数量验证的测试基础  
**适合人群**: 朋友做购物车测试时的参考  
**关键部分**:
- 原始版本(4个测试)和增强版本(12个测试)
- 详细的分区设计
- 测试结果分析

**建议阅读时间**: 15分钟  

---

### 【项目整体文档】📋 背景参考

#### 7. [PROJECT_TEST_REPORT.md](PROJECT_TEST_REPORT.md) ⭐⭐
**内容**: Shopizer 电子商务平台整体测试报告  
**用途**: 了解项目概貌  
**适合人群**: 初次接触项目的人  
**关键部分**:
- 项目概述 (什么是Shopizer?)
- 项目统计 (115K LOC, Spring Boot等)
- 构建文档 (如何编译运行)
- 现有测试文档 (4%覆盖率)
- 分区测试设计原理

**建议阅读时间**: 30分钟  
**行动项**: 
- [ ] 了解Shopizer的5个主要模块
- [ ] 了解现有的测试框架和工具

---

#### 8. [TESTING_GUIDE.md](TESTING_GUIDE.md) ⭐⭐⭐
**内容**: Shopizer 测试指南  
**用途**: 学习如何写测试  
**适合人群**: 需要测试最佳实践的人  
**关键部分**:
- 测试框架设置
- 基类使用(ServicesTestSupport)
- 如何写集成测试
- 常见测试模式
- 数据初始化方法

**建议阅读时间**: 30分钟  
**行动项**: 
- [ ] 理解ServicesTestSupport基类
- [ ] 学习如何使用TestRestTemplate

---

#### 9. [TEST_ENVIRONMENT_SETUP.md](TEST_ENVIRONMENT_SETUP.md) ⭐⭐
**内容**: 测试环境配置指南  
**用途**: 第一次运行测试时需要  
**适合人群**: 新成员或需要重新配置的人  
**关键部分**:
- Java版本要求
- Maven配置
- Spring Boot测试配置
- H2数据库配置
- 运行测试的命令

**建议阅读时间**: 10分钟  
**何时需要**: 首次设置开发环境

---

### 【其他分析文档】📊 补充资料

#### 10. [TEST_CLASS_ANALYSIS.md](TEST_CLASS_ANALYSIS.md)
**内容**: 测试类分析  
**用途**: 理解现有测试代码结构  

---

#### 11. [MyCartQuantityTest_Original_Backup.java](MyCartQuantityTest_Original_Backup.java)
**内容**: 原始购物车数量测试类备份  
**用途**: 参考代码实现  

---

### 【源代码】💻 实际代码

#### 12. [sm-shop/src/test/java](../sm-shop/src/test/java)
**内容**: 所有Java测试代码  
**关键测试类**:
```
sm-shop/src/test/java/com/salesmanager/test/shop/
├── common/
│   └── ServicesTestSupport.java        ← 基类,必读
├── integration/
│   ├── product/
│   │   ├── ProductManagementAPIIntegrationTest.java    ← 参考
│   │   └── ProductV2ManagementAPIIntegrationTest.java  ← 参考
│   ├── cart/
│   │   ├── ShoppingCartAPIIntegrationTest.java         ← 朋友的参考
│   │   └── CartTestBean.java                            ← 辅助类
│   ├── order/
│   │   └── OrderApiIntegrationTest.java                ← 参考
│   └── ...
└── util/
    └── GeneratePasswordTest.java
```

**建议阅读顺序**:
1. ServicesTestSupport.java (了解基础)
2. ShoppingCartAPIIntegrationTest.java (了解集成测试样式)
3. ProductManagementAPIIntegrationTest.java (了解产品API测试)

---

## 📚 按学习阶段的推荐阅读顺序

### 【阶段1】快速入门 (30分钟)

如果你只有半小时,按这个顺序:

1. **[WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md)** (15分钟)
   - 快速了解你的职责
   - 了解与朋友的分工

2. **[PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md)** - 第1和第2章 (15分钟)
   - 理解为什么选择产品上架
   - 看看FSM的概念
   - 扫一眼7个状态

**输出**: 你知道大致的方向

---

### 【阶段2】基础理解 (90分钟)

1. **[FEATURE_DIVISION_ANALYSIS.md](FEATURE_DIVISION_ANALYSIS.md)** (30分钟)
   - 完整了解架构和功能划分
   - 理解冲突点

2. **[PRODUCT_PRICE_TEST_REPORT_EN.md](PRODUCT_PRICE_TEST_REPORT_EN.md)** (30分钟)
   - 复习你现有的价格测试
   - 理解7个分区和边界值

3. **[PROJECT_TEST_REPORT.md](PROJECT_TEST_REPORT.md)** (30分钟)
   - 了解Shopizer项目

**输出**: 你能与朋友讨论清楚分工方案

---

### 【阶段3】详细规划 (120分钟)

1. **[PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md)** - 完整阅读 (60分钟)
   - 深入理解每个状态
   - 学习31个测试用例框架
   - 理解与价格测试的结合

2. **[TESTING_GUIDE.md](TESTING_GUIDE.md)** (30分钟)
   - 学习如何实现测试

3. **[sm-shop/src/test/java/...](../sm-shop/src/test/java)** 代码浏览 (30分钟)
   - 看看现有的测试代码

**输出**: 你有详细的实现计划

---

### 【阶段4】实现 (多天)

1. 创建 ProductLifecycleStateMachineTest.java
   - 参考 [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md) 的测试框架
   - 按类别实现31个测试用例

2. 编写FSM设计文档
   - 绘制状态图
   - 编写状态转移表
   - 说明价格的角色

3. 更新 PROJECT_TEST_REPORT.md
   - 添加FSM设计部分
   - 补充新增的31个测试用例

4. 推送到GitHub

**输出**: 完整的第二次作业提交

---

## 🔍 如何查找特定信息

### "我想了解价格测试的所有分区"
👉 [PRODUCT_PRICE_TEST_REPORT_EN.md](PRODUCT_PRICE_TEST_REPORT_EN.md) → 搜索 "Partition"  
👉 [PRODUCT_PRICE_TEST_REPORT_ZH.md](PRODUCT_PRICE_TEST_REPORT_ZH.md) → 搜索 "分区"

### "我想知道怎样避免与朋友的测试冲突"
👉 [WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md) → 冲突检查清单  
👉 [FEATURE_DIVISION_ANALYSIS.md](FEATURE_DIVISION_ANALYSIS.md) → 冲突分析部分

### "我想看第二次作业的完整框架"
👉 [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md) → 所有内容

### "我想了解产品上架的状态机"
👉 [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md) → 状态图部分

### "我想看现有的测试代码样例"
👉 [sm-shop/src/test/java/com/salesmanager/test/shop/integration/](../sm-shop/src/test/java/com/salesmanager/test/shop/integration/)

### "我不知道怎样运行测试"
👉 [TEST_ENVIRONMENT_SETUP.md](TEST_ENVIRONMENT_SETUP.md)  
👉 [TESTING_GUIDE.md](TESTING_GUIDE.md)

### "我想了解Shopizer的项目结构"
👉 [PROJECT_TEST_REPORT.md](PROJECT_TEST_REPORT.md) → 项目统计部分

---

## 📊 文档关系图

```
你要做的第二次作业
        ↓
[WORK_DIVISION_SUMMARY.md] ← 先看这个,了解分工
        ↓
[FEATURE_DIVISION_ANALYSIS.md] ← 理解为什么这样划分
        ↓
[PRODUCT_LISTING_FSM_DESIGN.md] ← 你的作业详细框架!
        ↓
参考你现有的工作:
├── [PRODUCT_PRICE_TEST_REPORT_EN.md]
├── [PRODUCT_PRICE_TEST_REPORT_ZH.md]
└── [PRODUCT_PRICE_TEST_REPORT.java] (源代码)
        ↓
参考现有的测试代码:
├── [ServicesTestSupport.java]
├── [ProductManagementAPIIntegrationTest.java]
└── ...

        ↓
[PROJECT_TEST_REPORT.md] ← 项目总体背景
[TESTING_GUIDE.md] ← 测试最佳实践
        ↓
实现你的测试!
```

---

## 📋 清单：你应该拥有的所有文件

在 `/test-reports/` 目录中,你应该看到:

```
test-reports/
├── 📄 PRODUCT_PRICE_TEST_REPORT_EN.md         ← 你的价格测试(英文)
├── 📄 PRODUCT_PRICE_TEST_REPORT_ZH.md         ← 你的价格测试(中文)
├── 📄 TEST_ENHANCEMENT_SUMMARY.md             ← 朋友的购物车扩展
├── 📄 PROJECT_TEST_REPORT.md                  ← 项目总体报告
├── 📄 TESTING_GUIDE.md                        ← 测试指南
├── 📄 TEST_ENVIRONMENT_SETUP.md               ← 环境配置
├── 📄 TEST_CLASS_ANALYSIS.md                  ← 测试类分析
├── 📄 MyCartQuantityTest_Original_Backup.java ← 购物车测试备份
│
├── 🆕 WORK_DIVISION_SUMMARY.md                ← 本索引关联的分工总结
├── 🆕 FEATURE_DIVISION_ANALYSIS.md            ← 功能划分详细分析
└── 🆕 PRODUCT_LISTING_FSM_DESIGN.md           ← FSM设计框架【重点!】
```

---

## ✅ 下一步行动

### 【立即做】第1优先级

- [ ] 阅读 [WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md)
- [ ] 与朋友讨论功能划分方案
- [ ] 在 WORK_DIVISION_SUMMARY.md 的清单中打勾确认

### 【今天做】第2优先级

- [ ] 完整阅读 [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md)
- [ ] 起草第二次作业的框架
- [ ] 列出31个测试用例的实现计划

### 【本周做】第3优先级

- [ ] 开始实现第一批测试用例 (状态转换测试)
- [ ] 创建 ProductLifecycleStateMachineTest.java
- [ ] 绘制产品状态机的状态图

### 【本月做】第4优先级

- [ ] 完成所有31个测试用例
- [ ] 编写FSM详细文档
- [ ] 提交到GitHub

---

## 🤝 与朋友的协作

### 建议与朋友一起讨论的话题

1. **分工方案** (参考 [WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md))
   - [ ] 你做产品价格+上架FSM
   - [ ] 他做购物车+订单流程FSM
   - [ ] 确认订单价格验证的处理方式

2. **代码协作** 
   - [ ] 测试数据如何隔离?
   - [ ] @BeforeEach 如何重置?
   - [ ] GitHub分支策略?

3. **文档同步**
   - [ ] 在共同参考文档中补充说明
   - [ ] 约定文档更新的频率

---

## 📞 常见问题

### Q: 我应该什么时候开始写代码?
**A**: 建议先完成【阶段3】(规划)再开始编码。这样能避免重复工作。

### Q: 如果与朋友的工作冲突了怎么办?
**A**: 参考 [WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md) 的"冲突检查清单"。大多数冲突可以通过明确的分工界线解决。

### Q: FSM是什么?不懂怎么办?
**A**: [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md) 的第2章有通俗的介绍。可以先看那里。

### Q: 31个测试用例太多了,能不能少一点?
**A**: 可以。但35%的工作量需要用测试用例来证明。建议至少做20个。

### Q: 现有的价格测试我可以直接用吗?
**A**: 可以!现有的7个分区+8个边界值测试可以直接集成到新的FSM测试框架中。

---

## 📖 总结

这套文档为你的第二次作业提供了:

✅ **清晰的分工方案** - 与朋友的工作如何协调  
✅ **详细的FSM框架** - 31个测试用例的完整设计  
✅ **现有工作的整合** - 如何利用已有的价格分区测试  
✅ **代码参考** - 现有的测试代码可以参考  
✅ **最佳实践** - 如何写好测试  

**关键文档顺序**: 
1. 分工 → 2. 功能划分 → 3. FSM设计 → 4. 实现

**预计时间**: 
- 规划: 2-3小时
- 实现: 1-2天
- 文档: 1天

**最终产出**:
- ProductLifecycleStateMachineTest.java (31+个测试)
- 完整的FSM设计文档
- 更新的项目测试报告

**祝你好运!** 🎓

---

**文档版本**: 1.0  
**最后更新**: 2026年2月7日  
**下一次审视**: 完成所有作业后
