# 你与朋友的功能测试分工 - 快速参考表

**日期**: 2026年2月7日  
**作业**: 软件测试第二次作业  
**项目**: Shopizer 电子商务平台

---

## 🎯 核心问题回答

### Q: 价格测试和购物车测试会不会冲突？

**A: 低风险，但需要明确划分**

```
价格测试 (你)          购物车测试 (朋友)
    ↓                      ↓
产品上架(创建价格) → 浏览产品(读取价格) → 加入购物车 → 结账(使用价格)
    │                                          ↑
    └──────── 价格流向 ─────────────────────────┘
```

**冲突点**: 订单创建时需要使用产品价格，两个人都可能涉及。

**解决方案**: 你负责**创建和验证**价格，朋友负责**使用和集成**价格。

---

## 📊 职责分工对比表

### 【你的职责】产品价格与上架 (Product Price & Listing)

| 模块 | API端点 | 测试类型 | 具体工作 | 优先级 |
|------|--------|--------|---------|-------|
| **产品上架** | `POST /api/v1/private/product?store=DEFAULT` | 集成测试 | 创建产品，设置价格 | ⭐⭐⭐ |
| **价格验证** | ProductPricePartitionTest | 单元测试 | 7个分区测试 | ⭐⭐⭐⭐⭐ |
| **价格更新** | `PUT /api/v1/private/product/{id}?store=DEFAULT` | 集成测试 | 修改产品价格，验证新价格 | ⭐⭐⭐ |
| **边界值测试** | 0.00, -0.01, 999999.99等 | 单元测试 | 8个边界值 | ⭐⭐⭐⭐ |
| **精度控制** | price.scale() <= 2 | 单元测试 | 禁止3位以上小数 | ⭐⭐⭐⭐ |
| **FSM状态转换** | DRAFT → PENDING → ACTIVE | 集成测试 | 产品生命周期管理 | ⭐⭐⭐⭐ |

**最终产出**:
- [ ] ProductPricePartitionTest.java (完整的分区和边界测试)
- [ ] ProductListingFSMTest.java (新增，状态机测试)
- [ ] PRODUCT_LISTING_FSM_DESIGN.md (FSM详细文档)
- [ ] 更新 PROJECT_TEST_REPORT.md 中的价格部分

---

### 【朋友的职责】购物车与订单 (Shopping Cart & Order)

| 模块 | API端点 | 测试类型 | 具体工作 | 优先级 |
|------|--------|--------|---------|-------|
| **添加购物车** | `POST /api/v1/cart/` | 集成测试 | 选择产品(已上架)，添加到购物车 | ⭐⭐⭐ |
| **数量验证** | quantity字段 | 分区测试 | 有效(1-库存)，无效(负数、零、超库存) | ⭐⭐⭐⭐⭐ |
| **修改购物车** | `PUT /api/v1/cart/{cartId}/product/{productId}` | 集成测试 | 修改商品数量或删除 | ⭐⭐⭐ |
| **创建订单** | `POST /api/v1/order/` | 集成测试 | 从购物车结账，生成订单 | ⭐⭐⭐⭐ |
| **订单验证** | 订单总价、每个商品价格 | 集成测试 | **验证**(不修改)价格计算正确性 | ⭐⭐⭐ |
| **购买流程FSM** | CART → PENDING → PAID → SHIPPED | 集成测试 | 订单生命周期 | ⭐⭐⭐⭐ |

**最终产出**:
- [ ] ShoppingCartQuantityFSMTest.java (完整的购物车流程测试)
- [ ] OrderProcessingTest.java (新增，订单测试)
- [ ] SHOPPING_CART_FSM_DESIGN.md (购物车FSM文档)
- [ ] 更新 PROJECT_TEST_REPORT.md 中的购物车部分

---

## 🚨 冲突风险矩阵

### 哪些功能可能重叠?

```
┌─────────────────┬──────────┬──────────┬──────────┐
│ 功能            │ 你的范围 │ 他的范围 │ 冲突风险 │
├─────────────────┼──────────┼──────────┼──────────┤
│ 产品创建        │ ✅ 核心  │ ❌      │ 无冲突   │
│ 产品价格设置    │ ✅ 核心  │ ❌      │ 无冲突   │
│ 产品价格查询    │ ✅       │ ✅ 使用 │ 低冲突   │
│ 产品浏览(前台)  │ ❌       │ ✅ 核心 │ 无冲突   │
│ 添加购物车      │ ❌       │ ✅ 核心 │ 无冲突   │
│ 购物车数量验证  │ ❌       │ ✅ 核心 │ 无冲突   │
│ 创建订单        │ ⚠️ 参与  │ ✅ 核心 │ 中冲突   │
│ 订单价格计算    │ ✅ 验证  │ ✅ 核心 │ **高冲突**│
│ 订单支付        │ ❌       │ ✅ 核心 │ 无冲突   │
│ 订单确认        │ ❌       │ ✅ 核心 │ 无冲突   │
└─────────────────┴──────────┴──────────┴──────────┘
```

### 【高冲突】订单价格计算的处理方式

**问题**: 订单中的商品总价涉及产品价格，两个人都关心

**解决方案** (优先级从高到低):

1. **方案A** (推荐): 功能测试分离，但集成点定义清楚
   ```
   你的职责:
     ├── 产品价格的有效性验证 ✅
     ├── 创建产品时设置的价格 ✅
     └── 价格修改的合法性验证 ✅
   
   他的职责:
     ├── 订单创建时的价格应用 ✅
     ├── 订单价格的正确性验证 ✅
     └── 购物车 → 订单的价格流转 ✅
   
   【关键点】: 你们分别写测试,但约定:
     - 他的测试中,产品价格必须来自你创建的有效产品
     - 他的测试验证价格被正确应用到订单
     - 如果订单价格计算错误,是他的问题(不是你的价格)
   ```

2. **方案B** (备选): 明确的分工界线
   ```
   你: 单元测试 ProductPriceService
     ├── isValidPrice(BigDecimal) → boolean
     ├── formatPrice(BigDecimal) → String
     └── calculateTax(price, taxRate) → BigDecimal
   
   他: 集成测试 OrderService
     ├── createOrder(cart) → Order
     ├── 使用你提供的isValidPrice()进行验证
     └── calculateOrderTotal(items) → BigDecimal
   ```

---

## 📋 推荐的第二次作业题目设计

### 你的题目

```
标题: "产品上架流程的有限状态机建模与价格验证测试"

描述: 
  针对Shopizer电商平台的产品上架功能,
  通过有限状态机(FSM)建模来描述产品的完整生命周期,
  并重点关注在各个状态转换中的价格验证。

工作量分配:
  - 10% (Finite Models Value): 
    论述FSM在e-commerce产品管理中的作用,
    为什么价格验证对状态转换至关重要
  
  - 20% (Feature Selection):
    选择"产品上架流程"作为功能模型,
    说明为什么它适合FSM建模
    (7个状态, 8个转换, 多个守卫条件)
  
  - 35% (Model Creation & Description):
    - 绘制完整的状态转移图(7个状态)
    - 详细描述每个状态的含义和操作
    - 阐述转换的守卫条件,特别是价格相关的条件
    - 提供状态转移表和转换规则
  
  - 35% (JUnit Test Cases):
    - 状态转换正确性测试(13个测试)
    - 价格分区测试(7个分区)
    - 边界值测试(8个测试)
    - 守卫条件测试(6个测试)
    - 端到端集成测试(5个测试)
    
    总计: 39+个测试用例,
    全部推送到GitHub,文档中有详细说明
```

### 朋友的题目(建议)

```
标题: "购物车和订单流程的有限状态机建模与数量验证测试"

工作量分配:
  - 10% (Finite Models Value)
  - 20% (Feature Selection): 购物车 + 订单流程
  - 35% (Model Creation): 状态图、转移表、约束条件
  - 35% (JUnit Tests): 
    - 购物车状态转换(数量验证为重点)
    - 订单处理流程
    - 价格集成验证(与你的产品协作)
```

---

## ✅ 冲突检查清单

在启动第二次作业前,请完成以下检查:

- [ ] **你**会专注于产品价格和上架功能,包括FSM建模
- [ ] **朋友**会专注于购物车和订单功能,包括数量验证
- [ ] 两个人使用不同的测试数据集(避免共享产品状态)
- [ ] 订单价格验证的界线明确:
  - [ ] 你: 创建和验证价格数据的合法性
  - [ ] 朋友: 验证价格在订单中被正确应用
- [ ] 测试执行时隔离:
  - [ ] 每个测试使用 @BeforeEach/@AfterEach 重置数据
  - [ ] 不依赖其他人的测试执行顺序
- [ ] 代码审查点:
  - [ ] ProductService 的修改由你负责审查
  - [ ] OrderService 的修改由朋友负责审查
- [ ] 文档同步:
  - [ ] 你的文档清楚说明价格测试的范围
  - [ ] 朋友的文档清楚说明购物车/订单的范围
  - [ ] 在冲突区域(订单价格)有明确说明

---

## 📚 相关文档参考

### 你应该阅读和扩展的文档

| 文档 | 用途 | 状态 |
|------|------|------|
| [PRODUCT_PRICE_TEST_REPORT_EN.md](PRODUCT_PRICE_TEST_REPORT_EN.md) | 你现有的价格测试详情 | ✅ 已有 |
| [PRODUCT_PRICE_TEST_REPORT_ZH.md](PRODUCT_PRICE_TEST_REPORT_ZH.md) | 中文版本 | ✅ 已有 |
| [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md) | 新增FSM设计 | ✅ 本文档提供 |
| [PROJECT_TEST_REPORT.md](PROJECT_TEST_REPORT.md) | 总体项目报告 | 📝 需要更新 |

### 朋友应该阅读的文档

| 文档 | 用途 | 状态 |
|------|------|------|
| [TEST_ENHANCEMENT_SUMMARY.md](TEST_ENHANCEMENT_SUMMARY.md) | 购物车测试基础 | ✅ 已有 |
| [ShoppingCartAPIIntegrationTest.java](../sm-shop/src/test/java/com/salesmanager/test/shop/integration/cart/ShoppingCartAPIIntegrationTest.java) | 现有购物车测试 | ✅ 已有 |
| [SHOPPING_CART_FSM_DESIGN.md](SHOPPING_CART_FSM_DESIGN.md) | 新增购物车FSM | 📝 需要编写 |

### 共同参考

| 文档 | 用途 | 状态 |
|------|------|------|
| [FEATURE_DIVISION_ANALYSIS.md](FEATURE_DIVISION_ANALYSIS.md) | 本文档(功能划分分析) | ✅ 已提供 |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | 测试指南 | ✅ 已有 |
| [TEST_ENVIRONMENT_SETUP.md](TEST_ENVIRONMENT_SETUP.md) | 环境配置 | ✅ 已有 |

---

## 🎓 给你朋友的建议(如果他愿意看的话)

### 购物车FSM的可能设计

```
状态:
  ├── EMPTY (空购物车,初始)
  ├── ACTIVE (有商品,可编辑)
  ├── LOCKED (已提交,禁止编辑)
  ├── PENDING_PAYMENT (待支付)
  ├── PAID (已支付)
  ├── SHIPPED (已发货)
  └── COMPLETED (已完成)

关键转换:
  EMPTY → ACTIVE 
    when addItem(product, quantity)
    guard: quantity in [1, inventory]  ← 他的数量分区测试
  
  ACTIVE → LOCKED
    when submitCheckout()
    guard: cartTotal > 0, allPricesValid ← 你的价格验证来这里!
  
  LOCKED → PENDING_PAYMENT
    when initiatePayment()
  
  等等...
```

### 关键的集成测试

```
@Test
public void testEndToEnd_CartToPaidOrder() {
  // 1. 创建产品(由你测试)
  Product p = productService.findByCode("TEST-001");
  assertNotNull(p.getPrice());  // 依赖你的价格是合法的
  
  // 2. 添加到购物车(他的责任)
  cart.addItem(p, 5);  // 依赖他的数量验证
  
  // 3. 结账(他的责任)
  Order order = orderService.createFromCart(cart);
  
  // 4. 验证订单价格正确(他的责任,但与你的价格数据相关)
  assertEquals(
    p.getPrice().multiply(BigDecimal.valueOf(5)),
    order.getTotalPrice()
  );
}
```

---

## 🔗 快速链接

- [功能划分详细分析](FEATURE_DIVISION_ANALYSIS.md)
- [产品上架FSM设计](PRODUCT_LISTING_FSM_DESIGN.md)
- [价格测试报告](PRODUCT_PRICE_TEST_REPORT_EN.md)
- [购物车增强文档](TEST_ENHANCEMENT_SUMMARY.md)
- [项目整体报告](PROJECT_TEST_REPORT.md)

---

**最后更新**: 2026年2月7日  
**版本**: 1.0  
**审核状态**: 待确认
