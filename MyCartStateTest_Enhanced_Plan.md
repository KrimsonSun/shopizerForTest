# Shopping Cart FSM 测试扩充方案（Yuqian Chiu）

## 当前状态
- 2个测试场景
- 3个状态（EMPTY, ACTIVE, OBSOLETE）
- 5个转换

## 扩充方案：增加到16个测试用例

### 分类1：状态验证测试（3个测试）
1. `testState1_EmptyCart()` - 验证EMPTY状态
2. `testState2_ActiveCart()` - 验证ACTIVE状态
3. `testState3_ObsoleteCart()` - 验证OBSOLETE状态

### 分类2：转换测试（5个测试）
4. `testTransition1_EmptyToActive_AddItem()` - EMPTY → ACTIVE
5. `testTransition2_ActiveSelfLoop_UpdateQuantity()` - ACTIVE → ACTIVE
6. `testTransition3_ActiveToEmpty_RemoveLastItem()` - ACTIVE → EMPTY
7. `testTransition4_EmptyToObsolete_DeleteEmptyCart()` - EMPTY → OBSOLETE
8. `testTransition5_ActiveToObsolete_DeleteActiveCart()` - ACTIVE → OBSOLETE

### 分类3：边界条件测试（4个测试）
9. `testBoundary1_MaxQuantityInCart()` - 测试最大数量
10. `testBoundary2_MultipleItemsInCart()` - 多商品场景
11. `testBoundary3_ZeroQuantity()` - 数量为0
12. `testBoundary4_NegativeQuantity()` - 负数数量（应失败）

### 分类4：无效转换测试（2个测试）
13. `testInvalid1_UpdateQuantityInEmptyCart()` - 在EMPTY状态更新数量
14. `testInvalid2_RemoveItemFromEmptyCart()` - 从EMPTY移除商品

### 分类5：完整场景测试（2个测试）
15. `testScenario1_CompleteLifecycle()` - 完整生命周期
16. `testScenario2_MultipleOperations()` - 多次操作序列

## 预期发现的缺陷（增加价值）
- BUG-CART-01: 允许负数数量
- BUG-CART-02: 数量为0时未自动移除商品
- BUG-CART-03: EMPTY状态可以执行更新操作

## 覆盖率对比
- 原始：2个场景，100%转换覆盖
- 扩充后：16个测试，100%转换 + 边界 + 无效操作 + 缺陷发现
