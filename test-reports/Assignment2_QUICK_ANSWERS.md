# 快速回答：你与朋友的功能测试分工问题
## Quick Answer: Work Division Q&A

---

## ❓ 核心问题 1: 价格测试和购物车测试会不会产生冲突?

### 直接答案

**大概率: 否。但需要注意一个关键点。**

```
你的工作:
  产品创建 (设置价格)
       ↓
  产品上架(验证价格)
       ↓
  已上架产品(显示在商城)

朋友的工作:
       ↓
  浏览产品(读取价格)
       ↓
  加入购物车
       ↓
  创建订单
       ↓
  订单中计算总价(使用你的价格数据)
```

**冲突点**: 订单总价计算

```
订单总价 = 产品价格 × 数量

你负责:  ✓ 产品价格是否合法(分区、边界值)
他负责:  ✓ 订单中的价格是否被正确应用
        ✓ 总价计算是否正确(price × quantity)
```

**如何避免冲突**: 
- 你写测试验证价格数据的有效性
- 他写测试验证价格数据在订单中的使用
- 两个人的测试数据隔离(各用各的产品)

---

## ❓ 核心问题 2: 功能测试是否应该分开?

### 直接答案

**是的。建议按照这样分工:**

```
【你的职责】产品价格与上架功能 (Product Price & Listing)
├── 测试范围: /api/v1/private/product/* (后台API)
├── 核心测试: 
│   ├── 产品创建时的价格验证 (分区测试)
│   ├── 产品上架流程的状态转换 (FSM)
│   ├── 价格修改的有效性检查 (边界值)
│   └── 无效价格的拒绝(P5负数, P6精度, P7null)
└── 产出物:
    ├── ProductLifecycleStateMachineTest.java (新增)
    ├── 7个产品状态的FSM模型
    ├── 31+个JUnit测试用例
    └── 完整的FSM文档

【朋友的职责】购物车与订单功能 (Shopping Cart & Order)
├── 测试范围: /api/v1/cart/* 和 /api/v1/order/* (前台API)
├── 核心测试:
│   ├── 购物车数量验证 (你朋友的现有MyCartQuantityTest)
│   ├── 购物车状态转换 (FSM)
│   ├── 订单创建流程
│   └── 订单价格计算正确性(使用你创建的有效产品)
└── 产出物:
    ├── ShoppingCartFSMTest.java (新增)
    ├── OrderProcessingTest.java (新增)
    ├── 购物车状态的FSM模型
    ├── 订单处理流程的FSM模型
    └── 完整的购物车/订单FSM文档
```

### 为什么这样分工好?

| 方面 | 好处 |
|------|------|
| **职责清晰** | 你管产品,他管购物流程 |
| **代码独立** | 你的测试独立,他的测试独立 |
| **冲突最小** | 交界点(订单价格)有清晰的分工 |
| **易于review** | 老师/TA容易审查每个人的工作 |
| **可复用** | 你的价格验证可以被他的测试复用 |

---

## ❓ 核心问题 3: 他应该负责购买请求,我负责上架请求,对吗?

### 直接答案

**是的,完全正确! 就是这个意思。**

```
请求类型对应:

你的上架请求 (Listing/Product Submission):
  └─ POST /api/v1/private/product?store=DEFAULT
     请求体: { name, description, price, stock, category }
     权限: 仅商家/管理员
     目的: 创建和管理产品目录
     重点: 价格数据的有效性

他的购买请求 (Purchase/Order):
  ├─ POST /api/v1/cart/
  │  请求体: { productId, quantity }
  │  权限: 任何用户(顾客)
  │  目的: 添加商品到购物车
  │
  └─ POST /api/v1/order/
     请求体: { cartId, paymentInfo, shippingAddress }
     权限: 顾客和系统
     目的: 将购物车转换为订单
     重点: 数量验证, 价格应用, 订单生成
```

### 具体的测试分工

```
【你的测试】上架请求相关:
  ✅ test_CreateProduct_ValidPrice
  ✅ test_CreateProduct_InvalidPrice_Negative
  ✅ test_CreateProduct_InvalidPrice_Precision
  ✅ test_SubmitProduct_CheckPriceValidation
  ✅ test_UpdateProduct_ModifyPrice
  ✅ test_RejectProduct_InvalidPrice

【他的测试】购买请求相关:
  ✅ test_AddToCart_ValidQuantity
  ✅ test_AddToCart_InvalidQuantity_Negative
  ✅ test_AddToCart_OverStock
  ✅ test_CreateOrder_VerifyPrice
  ✅ test_CreateOrder_CalculateTotalPrice
  ✅ test_ProcessOrder_PaymentFlow

【交界点】:
  ✅ test_E2E_ProductToCart_ThenOrder
     (他用你创建的产品进行测试)
```

---

## 📊 可视化分工图

### 整个电商流程

```
商家端                    顾客端
  │                        │
  ├─ 产品基础数据            │
  │  (名称、价格✓、库存)      │
  │  【你测试这部分】         │
  │                        │
  └─ 上架产品到商城            │
     (发起上架请求✓)          │
                           │
                           ├─ 浏览商城
                           │ (读取你创建的产品)
                           │
                           ├─ 加入购物车
                           │ (选择数量✓)
                           │ 【他测试这部分】
                           │
                           ├─ 结账
                           │ (发起购买请求✓)
                           │ 【他测试这部分】
                           │
                           └─ 生成订单
                             (使用产品价格✓)
                             (你验证价格有效)
                             (他验证价格应用正确)
                             【共同验证】
```

### 工作流程的关键点

```
step 1: 你 ← 创建产品,设置价格 ← 【你的职责】
        ↓
        验证价格: P1-P7分区, 8个边界值 ← 【你的测试】
        ↓
step 2: 产品上架,状态: DRAFT→PENDING→ACTIVE ← 【你的FSM】
        ↓
step 3: 他 ← 看到已上架的产品 ← 【他使用你的成果】
        ↓
        选择产品,数量: 1-库存 ← 【他的测试】
        ↓
step 4: 他 ← 加入购物车 ← 【他的职责】
        ↓
        验证: 有效数量, 总价 ← 【他的测试】
        ↓
step 5: 他 ← 创建订单 ← 【他的职责】
        ↓
        订单状态: PENDING→PAID→SHIPPED ← 【他的FSM】
        ↓
        验证: 订单价格 = 产品价格 × 数量 ← 【他的验证】
```

---

## 🎯 为什么要有限状态机(FSM)?

### 作业要求

老师要求你在第二次作业中:
1. 选择一个"适合用FSM描述的非平凡功能"
2. 创建、绘制和描述FSM
3. 写测试用例覆盖FSM

### 你的最佳选择: 产品上架流程 FSM

```
为什么选产品上架?

✅ 非平凡: 7个状态, 8个转换, 多个守卫条件
✅ 与价格相关: DRAFT→PENDING的转换需要价格验证
✅ 现实场景: 真实的电商平台都有这样的流程
✅ 容易测试: 每个状态转换都可以测试

产品状态转换:
  DRAFT (草稿)
    ↓ submitForApproval(需要price有效)
  PENDING (待审核)
    ├─ approve() → ACTIVE (已上架)
    └─ reject() → REJECTED (已拒绝)
  
  ACTIVE (已上架,可售)
    ├─ updatePrice() → MODIFIED (已修改,需重新审核)
    ├─ deactivate() → INACTIVE (已下架)
    └─ archive() → ARCHIVED (已归档)
```

### 他的可选选择: 购物车/订单 FSM

```
购物车状态:
  EMPTY → ACTIVE → LOCKED → PENDING_PAYMENT → PAID → SHIPPED → COMPLETED

订单状态:
  PENDING → PAID → SHIPPED → COMPLETED → ...

他也可以选择这个,作为他的第二次作业。
但建议主题是"数量验证与购物流程"。
```

---

## 📋 行动清单

### 【立即】(今天)

- [ ] 与朋友讨论这份分工方案
- [ ] 确认: 你做产品价格+上架FSM, 他做购物车+订单FSM
- [ ] 确认订单价格验证的界线:
  - 你: 创建和验证价格数据的合法性
  - 他: 验证价格在订单中被正确应用

### 【本周】

- [ ] 阅读完整的FSM设计文档: [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md)
- [ ] 起草第二次作业的框架
- [ ] 列出要实现的31个测试用例

### 【本月】

- [ ] 实现ProductLifecycleStateMachineTest.java
- [ ] 绘制产品状态机的状态图
- [ ] 完成FSM文档
- [ ] 推送到GitHub

---

## 🤝 与朋友的协作要点

### 需要一起讨论的3件事

1. **测试数据隔离**
   ```
   他的购物车测试需要一个有效的产品。
   建议: 让他在@BeforeEach中调用你的ProductService.create()
   避免: 直接共用同一个产品对象(可能产生状态污染)
   ```

2. **订单价格验证的分界**
   ```
   你: 测试ProductPricePartitionTest.java
   他: 测试OrderServiceTest.java中的价格应用
   
   如果订单价格计算错误:
   - 如果是价格数据本身错: 你的问题
   - 如果是价格应用逻辑错: 他的问题
   ```

3. **GitHub协作**
   ```
   建议:
   - 你创建分支: feature/product-listing-fsm
   - 他创建分支: feature/shopping-cart-fsm
   - 主分支: main或master
   - 定期merge避免冲突
   ```

---

## 📚 核心参考文档

| 文档 | 用途 | 优先级 |
|------|------|-------|
| [WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md) | 详细的分工说明 | ⭐⭐⭐⭐⭐ |
| [PRODUCT_LISTING_FSM_DESIGN.md](PRODUCT_LISTING_FSM_DESIGN.md) | 你的第二次作业框架 | ⭐⭐⭐⭐⭐ |
| [FEATURE_DIVISION_ANALYSIS.md](FEATURE_DIVISION_ANALYSIS.md) | 功能划分的深入分析 | ⭐⭐⭐⭐ |
| [PRODUCT_PRICE_TEST_REPORT_EN.md](PRODUCT_PRICE_TEST_REPORT_EN.md) | 你现有的价格测试 | ⭐⭐⭐ |
| [TEST_ENHANCEMENT_SUMMARY.md](TEST_ENHANCEMENT_SUMMARY.md) | 朋友的购物车测试基础 | ⭐⭐⭐ |

---

## ✅ 总结

### 你的问题 → 答案

**Q1: 价格测试和购物车测试会不会冲突?**
> A: 不会,只要分工清楚。你创建和验证价格,他使用和集成价格。

**Q2: 功能测试是否应该分开?**
> A: 是的。你做产品(上架请求),他做购物车(购买请求)。

**Q3: 他应该负责购买请求,我负责上架请求,对吗?**
> A: 完全正确!就是这个意思。

### 下一步

1. **与朋友分享** 这份文档和分工方案
2. **一起阅读** [WORK_DIVISION_SUMMARY.md](WORK_DIVISION_SUMMARY.md)
3. **做出承诺** 确认各自的职责
4. **开始规划** 各自的第二次作业

### 预期成果

你的第二次作业:
- ProductLifecycleStateMachineTest.java (31+个测试)
- 完整的FSM设计文档
- 状态转移图和约束条件说明

他的第二次作业:
- ShoppingCartFSMTest.java 或 OrderProcessingTest.java
- 完整的购物流程FSM设计文档

两个人的工作:
- 清晰的分工,避免冲突
- 可以相互参考和学习
- 最终都能获得好成绩

---

**祝你们的合作愉快!** 🎓📚

**版本**: 1.0  
**日期**: 2026年2月7日
