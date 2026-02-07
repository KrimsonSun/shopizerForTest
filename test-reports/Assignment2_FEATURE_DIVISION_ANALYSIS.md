# Shopizer 作业二 - 功能划分与冲突分析报告

**分析日期**: 2026年2月7日  
**课程**: 软件测试  
**项目**: Shopizer 电子商务平台  

---

## 📋 目录

1. [架构概览](#架构概览)
2. [现有功能划分](#现有功能划分)
3. [你的价格测试部分](#你的价格测试部分)
4. [朋友的购物车部分](#朋友的购物车部分)
5. [冲突分析](#冲突分析)
6. [建议的功能划分方案](#建议的功能划分方案)
7. [有限状态机(FSM)建议](#有限状态机fsm建议)

---

## 架构概览

### Shopizer 核心架构

```
┌─────────────────────────────────────────────────────┐
│         Shopizer E-commerce Platform (v3.2.5)       │
│                 Spring Boot 2.5.12                  │
└─────────────────────────────────────────────────────┘
        │
        ├─── sm-core-model (领域模型)
        │     ├── Product (产品)
        │     ├── Order (订单)
        │     ├── ShoppingCart (购物车)
        │     └── Customer (顾客)
        │
        ├─── sm-core (业务逻辑)
        │     ├── ProductService
        │     ├── ShoppingCartService
        │     ├── OrderService
        │     └── InventoryService
        │
        └─── sm-shop (REST API)
              ├── /api/v1/product/* (产品API)
              ├── /api/v1/cart/* (购物车API)
              ├── /api/v1/order/* (订单API)
              └── /api/v1/private/product/* (后台上架API)
```

### 测试框架堆栈

- **单元测试**: JUnit 4/5
- **集成测试**: Spring Boot Test + TestRestTemplate
- **测试基类**: `ServicesTestSupport` (处理认证、数据初始化)
- **测试覆盖率**: 当前约4%

---

## 现有功能划分

### 你的部分：产品价格测试 (Your: Product Price Testing)

**当前状态**: ✅ 已启动

#### 已完成工作:
- ✅ [PRODUCT_PRICE_TEST_REPORT_EN.md](PRODUCT_PRICE_TEST_REPORT_EN.md) - 详细的分区测试报告
- ✅ [PRODUCT_PRICE_TEST_REPORT_ZH.md](PRODUCT_PRICE_TEST_REPORT_ZH.md) - 中文版本
- ✅ ProductPricePartitionTest.java - 完整的JUnit测试类

#### 测试范围:
| 功能 | 测试端点 | 测试类型 | 状态 |
|------|--------|--------|------|
| 产品创建(含价格) | `POST /api/v1/private/product?store=DEFAULT` | 集成测试 | ✅ |
| 价格有效性验证 | ProductPricePartitionTest | 单元测试 | ✅ |
| 价格分区测试 | 7个分区 + 边界值 | 等价类划分 | ✅ |
| 零价格(促销) | Partition 1 | ✅ 通过 | ✅ |
| 正常价格范围 | Partition 2-3 | ✅ 通过 | ✅ |
| 负数价格(无效) | Partition 5 | ❌ 预期失败 | ⚠️ 发现bug |
| 精度验证(>2位小数) | Partition 6 | ⚠️ 需要处理 | ⚠️ |
| 空值处理 | Partition 7 | ❌ 预期失败 | ⚠️ |

#### 涉及的API端点:
```
# 产品创建(包含价格)
POST /api/v1/private/product?store=DEFAULT
请求体: PersistableProduct (包含 price: BigDecimal)

# 产品查询
GET /api/v1/product/{id}
响应体: ReadableProduct (包含 price)
```

#### 涉及的业务模块:
- **sm-core**: `ProductService`, `ProductService.createProduct()`
- **sm-shop**: `ProductController` (REST API)
- **sm-shop-model**: `PersistableProduct`, `PersistableProductPrice`

---

### 朋友的部分：购物车测试 (Friend's: Shopping Cart Testing)

**当前状态**: 📝 计划中

#### 已有的测试基础:
- ✅ [ShoppingCartAPIIntegrationTest.java](../sm-shop/src/test/java/com/salesmanager/test/shop/integration/cart/ShoppingCartAPIIntegrationTest.java) - 购物车集成测试
- ✅ [MyCartQuantityTest.java](../test-reports/MyCartQuantityTest_Original_Backup.java) - 数量验证测试
- ✅ [TEST_ENHANCEMENT_SUMMARY.md](TEST_ENHANCEMENT_SUMMARY.md) - 购物车测试增强文档

#### 购物车测试范围 (可扩展):
| 功能 | 测试端点 | 测试类型 | 建议 |
|------|--------|--------|------|
| 添加商品到购物车 | `POST /api/v1/cart/` | 集成测试 | ✅ 已有 |
| 数量验证 | 数量字段验证 | 分区测试 | ✅ 已有 |
| 更新购物车商品 | `PUT /api/v1/cart/{cartId}/product/{productId}` | 集成测试 | ✅ 已有 |
| 删除购物车商品 | `DELETE /api/v1/cart/{cartId}/product/{productId}` | 集成测试 | ✅ 已有 |
| 购物车结账 | `POST /api/v1/order/` (从购物车) | 集成测试 | ❓ 待划分 |
| **订单创建** | `POST /api/v1/order/` | 集成测试 | ❌ 可能冲突 |
| **订单查询** | `GET /api/v1/order/{id}` | 集成测试 | ❌ 可能冲突 |

#### 涉及的API端点:
```
# 购物车操作
POST /api/v1/cart/                                      # 创建/添加
PUT /api/v1/cart/{cartId}/product/{productId}          # 更新
DELETE /api/v1/cart/{cartId}/product/{productId}       # 删除
GET /api/v1/cart/{cartId}                              # 查询

# 订单操作（与购物车相关）
POST /api/v1/order/                                     # 创建订单
GET /api/v1/order/{id}                                  # 查询订单
```

#### 涉及的业务模块:
- **sm-core**: `ShoppingCartService`, `OrderService`
- **sm-shop**: `ShoppingCartController`, `OrderController`
- **sm-shop-model**: `PersistableShoppingCartItem`, `ReadableShoppingCart`

---

## 冲突分析

### 🚨 潜在冲突点

#### 1. **订单功能的重叠** (HIGH PRIORITY)

**冲突位置**: `/api/v1/order/*` 端点

```
你的部分：
  - 产品价格 → 产品创建(包含价格)

朋友的部分：
  - 购物车 → 订单创建(从购物车结账)

潜在冲突：
  订单中包含商品，每个商品都有价格 
  ↓
  订单创建/修改时，涉及产品价格的计算、验证、更新
  ↓
  两个人可能都需要测试订单相关功能
```

**具体场景:**
- 你创建产品时设置价格 → 朋友创建订单时使用这个价格
- 购物车商品总价计算依赖于产品价格的精度和有效性
- 订单确认时需要重新验证价格的正确性

#### 2. **产品库存与数量的关系** (MEDIUM PRIORITY)

```
购物车测试：
  - 测试添加商品数量(1-10个)
  - 测试超库存场景(>10个)

产品测试：
  - 产品创建时设置库存
  - 库存是否受价格影响？

关键问题：
  购物车中的商品数量是否应该影响产品价格计算？
```

#### 3. **测试数据的独立性问题** (MEDIUM PRIORITY)

```
两个测试都涉及：
  - 创建产品（你负责价格部分）
  - 将产品加入购物车（朋友负责）
  - 生成订单（重叠区域）

风险：
  - 如果共用同一个产品对象，价格修改可能影响另一测试
  - 测试执行顺序可能产生依赖
  - 并发测试时可能出现数据竞争
```

---

## 建议的功能划分方案

### ✅ 方案一: 基于工作流的完全分离 (推荐)

```
你的职责 (价格和产品上架):
├── 产品上架端点测试
│   ├── POST /api/v1/private/product?store=DEFAULT
│   ├── PUT /api/v1/private/product/{id}?store=DEFAULT
│   ├── GET /api/v1/private/products?store=DEFAULT
│   └── 后台产品管理相关API
│
├── 产品价格功能测试
│   ├── 产品创建时的价格设置
│   ├── 价格有效性验证(分区测试)
│   ├── 价格精度控制(边界值)
│   ├── 价格更新功能
│   └── 价格为零的促销产品
│
└── 产品目录管理
    ├── 产品分类
    ├── 产品详情(包含价格)
    └── 库存管理(与价格无关的部分)

---

朋友的职责 (购物车和购买流程):
├── 购物车操作API测试
│   ├── POST /api/v1/cart/
│   ├── PUT /api/v1/cart/{cartId}/product/{productId}
│   ├── DELETE /api/v1/cart/{cartId}/product/{productId}
│   └── GET /api/v1/cart/{cartId}
│
├── 购物车数量验证(分区测试)
│   ├── 有效数量范围(1-库存量)
│   ├── 无效数量(负数、零)
│   ├── 超库存数量
│   └── 多商品购物车
│
├── 结账和订单创建API测试
│   ├── POST /api/v1/order/ (从购物车创建)
│   ├── 订单确认
│   ├── 订单支付
│   └── 订单跟踪
│
└── 购物流程的端到端测试
    ├── 选择产品(浏览)
    ├── 添加到购物车
    ├── 修改数量
    ├── 结账
    └── 订单确认

---

【边界线】明确分工：

产品侧(你):
  - 产品上架请求: POST /api/v1/private/product (【你的职责】)
  - 上架时的价格设置: price字段验证 (【你的职责】)

购买侧(朋友):
  - 浏览已上架的产品: GET /api/v1/product (【朋友使用你的产品】)
  - 加入购物车: POST /api/v1/cart (【朋友的职责】)
  - 创建订单: POST /api/v1/order (【朋友的职责】)
  - 验证订单中的价格正确性: 【朋友验证，但不修改】
```

### 详细的职责分工表格

| 功能模块 | API 端点 | 你的职责 | 朋友的职责 | 冲突风险 |
|---------|---------|--------|----------|--------|
| **产品上架** | POST /api/v1/private/product | ✅ 负责 | ✅ 使用 | 低 |
| **产品价格设置** | price 字段 | ✅ **核心** | ✅ 验证 | **中** |
| **产品价格更新** | PUT /api/v1/private/product/{id} | ✅ 负责 | ❌ 禁止 | 低 |
| **产品查询(前台)** | GET /api/v1/product/{id} | ✅ 参与测试 | ✅ 负责 | 低 |
| **添加购物车** | POST /api/v1/cart/ | ❌ | ✅ 负责 | 低 |
| **购物车数量验证** | quantity 字段 | ❌ | ✅ 负责 | 低 |
| **创建订单** | POST /api/v1/order/ | ❌ | ✅ **核心** | **中** |
| **订单价格计算** | 订单总价 | ✅ 参与 | ✅ **核心** | **高** |
| **订单支付** | payment 相关 | ❌ | ✅ 负责 | 低 |

---

### ⚠️ 方案二: 基于模块层次的分离 (备选)

**如果方案一太复杂，可以考虑:**

```
你(产品目录模块):
  - 所有 /api/v1/private/product/* 端点(后台)
  - ProductService 的单元测试
  - 产品价格、库存、分类的一切测试

朋友(购物/订单模块):
  - 所有 /api/v1/cart/* 和 /api/v1/order/* 端点(前台)
  - ShoppingCartService 和 OrderService 的单元测试
  - 购物车、订单、支付的一切测试

【问题】: 朋友的订单创建会涉及你的产品数据，仍然有冲突
```

---

## 有限状态机(FSM)建议

作业要求你选择一个"适合用FSM描述的非平凡功能组件"。以下是两个很好的选择：

### 📊 选项一: 产品上架流程 FSM (推荐你做)

**为什么适合FSM:**
- 产品有明确的生命周期状态
- 状态转换有明确的条件和规则
- 涉及价格、库存、分类等多个字段的验证

**状态图:**

```
                    ┌─────────────────────┐
                    │  产品创建(Draft)    │  初始状态
                    │  - 设置基本信息     │
                    │  - 设置价格         │  【你的测试重点】
                    │  - 设置库存         │
                    └──────────┬──────────┘
                               │ 验证通过
                    ┌──────────▼──────────┐
                    │  待上架(Pending)    │
                    │  - 等待商家审核     │
                    │  - 审批
                    │  - 可能拒绝
                    └──────────┬──────────┘
                               │ 审批通过
                    ┌──────────▼──────────┐
                    │  已上架(Active)     │  ✅ 正常状态
                    │  - 可被购买         │
                    │  - 显示在商城       │
                    │  - 库存可用
                    └──────────┬──────────┘
                               │ 更新价格/库存
                    ┌──────────▼──────────┐
                    │  已修改(Modified)   │
                    │  - 价格/库存已变更  │
                    │  - 需要重新审核     │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │ 下架                 │ 重新提交审核
        ▼                      ▼
    ┌────────────┐      ┌─────────────┐
    │Inactive    │      │ Pending     │
    │(已下架)    │      │ (重新审核)  │
    └────────────┘      └─────────────┘
```

**涉及的约束条件 (Transition Guards):**

```java
// 从 Draft → Pending
Transition guard: {
  - price >= 0.00 && price <= 999999.99  // 你的价格测试覆盖
  - price precision <= 2 decimals         // 你的精度测试覆盖
  - name != null && name.length >= 2     
  - stock >= 0
  - category != null
}

// 从 Pending → Active (仅商家/管理员)
Transition guard: {
  - approval_status == APPROVED
  - all validation constraints met
}

// 从 Active → Modified
Transition guard: {
  - price changed OR stock changed
  - other_attributes unchanged
}

// 从 Active/Modified → Inactive
Transition guard: {
  - merchant.canDeactivate() == true
  - no active orders using this product
}
```

**JUnit测试用例框架:**

```java
public class ProductLifecycleStateMachineTest {
    
    // 测试状态转换的有效性
    @Test
    public void testValidTransition_DraftToPending() {
        // 创建有效产品(价格合法)
        Product p = createProduct(price=29.99);
        assertEquals(ProductStatus.DRAFT, p.getStatus());
        
        p.submitForApproval();
        assertEquals(ProductStatus.PENDING, p.getStatus());
    }
    
    // 测试无效的状态转换
    @Test(expected = InvalidStateTransitionException.class)
    public void testInvalidTransition_DraftToActive() {
        Product p = createProduct(price=-10.00);  // 无效价格
        p.approve();  // 不能直接从DRAFT跳到ACTIVE
    }
    
    // 测试状态转换的守卫条件
    @Test(expected = InvalidPriceException.class)
    public void testGuardCondition_NegativePrice() {
        Product p = createProduct(price=-10.00);
        p.submitForApproval();  // 应该因价格无效而失败
    }
    
    // 你的价格测试与FSM的结合
    @Test
    public void testPricePartitions_WithStateMachine() {
        // P1: Zero price
        Product p1 = createProduct(price=0.00);
        assertTrue(p1.canTransitionTo(ProductStatus.PENDING));
        
        // P2: Normal price
        Product p2 = createProduct(price=29.99);
        assertTrue(p2.canTransitionTo(ProductStatus.PENDING));
        
        // P5: Negative price (Invalid)
        Product p5 = createProduct(price=-10.00);
        assertFalse(p5.canTransitionTo(ProductStatus.PENDING));
    }
}
```

---

### 📊 选项二: 购物车状态机 FSM (你朋友可以做)

**状态图:**

```
┌─────────────────┐
│  空购物车       │ 初始状态
│ (Empty)         │
└────────┬────────┘
         │ 添加商品
┌────────▼────────┐
│  有商品          │ ✅ 正常使用
│ (Active)        │ - 可添加/删除/修改
└────────┬────────┘
         │ 清空购物车
┌────────▼────────┐
│  已清空          │
│ (Cleared)       │
└─────────────────┘
         │ 确认结账
┌────────▼────────┐
│  待确认          │
│ (PendingCheckout)│
└────────┬────────┘
         │ 完成支付
┌────────▼────────┐
│  已完成          │
│ (Completed)     │
└─────────────────┘
```

---

## 总结与建议

### 🎯 你应该做什么 (Product Price Testing)

**第二次作业的建议题目:**

> "产品上架功能的价格验证与有限状态机建模"

**包含内容:**

1. **10%** - 有限模型在测试中的价值
   - 解释FSM为什么在产品管理中有用
   - 讨论价格验证的复杂性

2. **20%** - 选择产品上架流程为功能模型
   - 解释为什么产品生命周期适合FSM
   - 阐述价格在各个状态中的作用

3. **35%** - 创建和描述FSM
   - 产品的7个状态
   - 转换条件与价格的关系
   - 状态图(UML或其他工具)

4. **35%** - JUnit测试用例
   ```
   ├── 价格分区测试 (利用你现有的成果)
   ├── 状态转换测试 (新增)
   │   ├── 有效转换
   │   ├── 无效转换
   │   └── 守卫条件验证
   └── 端到端集成测试
   ```

---

### 🎯 你朋友应该做什么 (Shopping Cart Testing)

**建议题目:**

> "购物车功能的需求分析与有限状态机测试"

**包含内容:**

1. **10%** - 有限模型在购物车测试中的应用
2. **20%** - 购物车状态流转
3. **35%** - FSM设计(包括数量验证)
4. **35%** - JUnit测试
   ```
   ├── 数量验证分区测试 (已有MyCartQuantityTest基础)
   ├── 状态转换测试
   └── 购物车到订单的流程测试
   ```

---

### ✅ 避免冲突的清单

- [ ] 你测试 `POST /api/v1/private/product` (后台上架)
- [ ] 朋友测试 `POST /api/v1/cart` (购物车)
- [ ] 你负责产品价格的所有验证
- [ ] 朋友负责购物车数量的所有验证
- [ ] 订单相关测试由朋友负责，你只验证价格数据的正确性
- [ ] 使用不同的测试数据集(你用你的产品，朋友用他的产品)
- [ ] 约定测试执行的隔离策略(使用@BeforeEach重置数据)
- [ ] 明确的代码review检查点

---

## 附录：现有测试文件参考

### 你的当前工作:
- [PRODUCT_PRICE_TEST_REPORT_EN.md](PRODUCT_PRICE_TEST_REPORT_EN.md)
- [PRODUCT_PRICE_TEST_REPORT_ZH.md](PRODUCT_PRICE_TEST_REPORT_ZH.md)
- [TEST_ENVIRONMENT_SETUP.md](TEST_ENVIRONMENT_SETUP.md)

### 你朋友可以参考:
- [ShoppingCartAPIIntegrationTest.java](../sm-shop/src/test/java/com/salesmanager/test/shop/integration/cart/ShoppingCartAPIIntegrationTest.java)
- [TEST_ENHANCEMENT_SUMMARY.md](TEST_ENHANCEMENT_SUMMARY.md)

### 公共资源:
- [PROJECT_TEST_REPORT.md](PROJECT_TEST_REPORT.md) - 总体项目测试文档
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - 测试指南

---

**编写者**: AI Assistant  
**审核状态**: 待确认  
**版本**: 1.0
