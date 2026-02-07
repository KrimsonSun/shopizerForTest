package com.salesmanager.test.shoppingcart;

import com.salesmanager.core.business.services.catalog.category.CategoryService;
import com.salesmanager.core.business.services.catalog.product.ProductService;
import com.salesmanager.core.business.services.catalog.product.type.ProductTypeService;
import com.salesmanager.core.business.services.catalog.product.manufacturer.ManufacturerService;
import com.salesmanager.core.business.services.merchant.MerchantStoreService;
import com.salesmanager.core.business.services.reference.language.LanguageService;
import com.salesmanager.core.business.services.shoppingcart.ShoppingCartService;
import com.salesmanager.core.model.catalog.category.Category;
import com.salesmanager.core.model.catalog.category.CategoryDescription;
import com.salesmanager.core.model.catalog.product.Product;
import com.salesmanager.core.model.catalog.product.availability.ProductAvailability;
import com.salesmanager.core.model.catalog.product.description.ProductDescription;
import com.salesmanager.core.model.catalog.product.manufacturer.Manufacturer;
import com.salesmanager.core.model.catalog.product.manufacturer.ManufacturerDescription;
import com.salesmanager.core.model.catalog.product.price.ProductPrice;
import com.salesmanager.core.model.catalog.product.type.ProductType;
import com.salesmanager.core.model.merchant.MerchantStore;
import com.salesmanager.core.model.reference.language.Language;
import com.salesmanager.core.model.shoppingcart.ShoppingCart;
import com.salesmanager.core.model.shoppingcart.ShoppingCartItem;
import com.salesmanager.test.common.AbstractSalesManagerCoreTestCase;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import javax.inject.Inject;
import java.math.BigDecimal;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

/**
 * FSM State Transition Test for Shopping Cart
 * Flow: Empty <-> Active -> Obsolete
 */
public class MyCartStateTest extends AbstractSalesManagerCoreTestCase {

    @Inject private ProductService productService;
    @Inject private ShoppingCartService shoppingCartService;
    @Inject private CategoryService categoryService;
    @Inject private ManufacturerService manufacturerService;
    @Inject private ProductTypeService productTypeService;
    @Inject private LanguageService languageService;
    @Inject private MerchantStoreService merchantStoreService;

    private MerchantStore store;
    private Product product;

    @Before
    public void setup() throws Exception {
        // 1. 取得預設商店
        store = merchantStoreService.getByCode(MerchantStore.DEFAULT_STORE);
        Language en = languageService.getByCode("en");

        // 2. 建立分類、廠商
        Category category = new Category();
        category.setMerchantStore(store);
        category.setCode("test-cat-fsm-" + System.currentTimeMillis());

        CategoryDescription catDesc = new CategoryDescription();
        catDesc.setName("Test Category");
        catDesc.setLanguage(en);
        catDesc.setCategory(category);
        category.setDescriptions(new HashSet<>(Set.of(catDesc)));
        categoryService.create(category);

        Manufacturer manufacturer = new Manufacturer();
        manufacturer.setMerchantStore(store);
        manufacturer.setCode("test-manuf-fsm-" + System.currentTimeMillis());

        ManufacturerDescription manufDesc = new ManufacturerDescription();
        manufDesc.setName("Test Manuf");
        manufDesc.setLanguage(en);
        manufDesc.setManufacturer(manufacturer);
        manufacturer.setDescriptions(new HashSet<>(Set.of(manufDesc)));
        manufacturerService.create(manufacturer);

        // 3. 建立商品
        ProductType productType = productTypeService.getProductType(ProductType.GENERAL_TYPE);

        product = new Product();
        product.setProductHeight(new BigDecimal(4));
        product.setProductLength(new BigDecimal(3));
        product.setProductWidth(new BigDecimal(1));
        product.setSku("TEST-SKU-FSM-" + System.currentTimeMillis());
        product.setManufacturer(manufacturer);
        product.setType(productType);
        product.setMerchantStore(store);

        // 4. 設定庫存 (Availability)
        ProductAvailability availability = new ProductAvailability();
        availability.setProductDateAvailable(new Date());
        availability.setProductQuantity(100);
        availability.setRegion("*");
        availability.setProduct(product);

        // 5. 設定價格 (Price)
        ProductPrice dprice = new ProductPrice();
        dprice.setDefaultPrice(true);
        dprice.setProductPriceAmount(new BigDecimal(29.99));
        dprice.setProductAvailability(availability);

        // 把價格加入庫存清單，不然系統找不到價格會報錯！
        availability.getPrices().add(dprice);

        ProductDescription description = new ProductDescription();
        description.setName("Test Product for FSM");
        description.setLanguage(en);
        description.setProduct(product);

        product.getDescriptions().add(description);
        product.getAvailabilities().add(availability);
        product.getCategories().add(category);

        productService.create(product);
    }

    @Test
    public void testShoppingCartFSM() throws Exception {

        // ==========================================
        // State 1: EMPTY (In-Memory Check)
        // ==========================================
        ShoppingCart cart = new ShoppingCart();
        cart.setMerchantStore(store);
        cart.setShoppingCartCode(UUID.randomUUID().toString());

        // 驗證: 確保新建立的物件是空的
        Assert.assertNotNull("Cart object created", cart);
        Assert.assertTrue("State should be EMPTY", cart.getLineItems() == null || cart.getLineItems().isEmpty());
        System.out.println(" State 1 Verified: EMPTY (In-Memory Check)");

        // ==========================================
        // Transition: addItem() -> State: ACTIVE
        // ==========================================
        ShoppingCartItem item = new ShoppingCartItem(cart, product);
        item.setQuantity(1);

        // Add item & Save
        cart.getLineItems().add(item);
        shoppingCartService.saveOrUpdate(cart);

        // 驗證: 確保資料庫裡有這台車，而且有商品
        ShoppingCart stateActive = shoppingCartService.getByCode(cart.getShoppingCartCode(), store);
        Assert.assertNotNull("Cart should exist in DB now (Active)", stateActive);
        Assert.assertFalse("State should be ACTIVE (not empty)", stateActive.getLineItems().isEmpty());
        System.out.println(" State 2 Verified: ACTIVE (Item Added & Saved)");

        // ==========================================
        // Transition: updateQty() -> State: ACTIVE (Self-Loop)
        // ==========================================
        ShoppingCartItem itemToUpdate = stateActive.getLineItems().iterator().next();
        itemToUpdate.setQuantity(2);
        shoppingCartService.saveOrUpdate(stateActive);

        ShoppingCart stateActiveSelf = shoppingCartService.getByCode(cart.getShoppingCartCode(), store);
        Assert.assertEquals(2, stateActiveSelf.getLineItems().iterator().next().getQuantity().intValue());
        System.out.println(" State 2 (Self-Loop) Verified: ACTIVE (Qty Updated)");

        // ==========================================
        // Transition: removeItem() -> State: EMPTY
        // ==========================================
        shoppingCartService.deleteShoppingCartItem(itemToUpdate.getId());

        // 驗證: 變回 Empty
        ShoppingCart stateBackToEmpty = shoppingCartService.getByCode(cart.getShoppingCartCode(), store);
        if (stateBackToEmpty != null) {
            Assert.assertTrue("State should be back to EMPTY", stateBackToEmpty.getLineItems() == null || stateBackToEmpty.getLineItems().isEmpty());
        }
        System.out.println(" State 1 (Return) Verified: EMPTY");

        // ==========================================
        // Transition: deleteCart() -> State: OBSOLETE
        // ==========================================
        if (stateBackToEmpty != null) {
            shoppingCartService.deleteCart(stateBackToEmpty);
        }

        ShoppingCart stateObsolete = shoppingCartService.getByCode(cart.getShoppingCartCode(), store);
        Assert.assertNull("State should be OBSOLETE (null)", stateObsolete);
        System.out.println(" State 3 Verified: OBSOLETE");
    }
    /**
     * Test Case 2: Verify the shortcut transition from ACTIVE directly to OBSOLETE
     * Flow: Create -> Add Item (Active) -> Delete Cart (Obsolete)
     */
    @Test
    public void testActiveToObsolete() throws Exception {
        System.out.println("====== Starting Test Case 2: ACTIVE -> OBSOLETE ======");

        // 1. 快速建立一個 Active 狀態的購物車
        ShoppingCart cart = new ShoppingCart();
        cart.setMerchantStore(store);
        cart.setShoppingCartCode(UUID.randomUUID().toString());

        ShoppingCartItem item = new ShoppingCartItem(cart, product);
        item.setQuantity(1);
        cart.getLineItems().add(item);

        // 直接存檔讓它變 Active
        shoppingCartService.saveOrUpdate(cart);

        // 驗證: 它是 Active 的
        ShoppingCart stateActive = shoppingCartService.getByCode(cart.getShoppingCartCode(), store);
        Assert.assertNotNull(stateActive);
        Assert.assertFalse("Should be ACTIVE", stateActive.getLineItems().isEmpty());
        System.out.println(" State Verified: ACTIVE (Has items)");

        // 2. 關鍵動作: 直接從 Active 狀態呼叫 deleteCart
        // 這就是你原本測不到的那條線！
        shoppingCartService.deleteCart(stateActive);

        // 3. 驗證: 應該要直接變 Obsolete (找不到)
        ShoppingCart stateObsolete = shoppingCartService.getByCode(cart.getShoppingCartCode(), store);
        Assert.assertNull("Should be OBSOLETE (null) after deleting an active cart", stateObsolete);
        System.out.println(" Transition Verified: ACTIVE -> OBSOLETE");
        System.out.println("=======================================================");
    }
}