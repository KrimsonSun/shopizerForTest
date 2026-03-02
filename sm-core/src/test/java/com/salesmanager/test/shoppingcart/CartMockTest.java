package com.salesmanager.test.shoppingcart;

import static org.mockito.Mockito.*;
import static org.junit.Assert.*;
import org.junit.Test;
import org.mockito.Mockito;
import java.math.BigDecimal;
import com.salesmanager.core.business.services.catalog.pricing.PricingService;
import com.salesmanager.core.business.services.shoppingcart.ShoppingCartService;
import com.salesmanager.core.model.order.OrderSummary;

public class CartMockTest {

    @Test
    public void testTotalCalculationWithMockedPrice() {
        PricingService mockPricing = Mockito.mock(PricingService.class);

        when(mockPricing.calculatePriceQuantity(any(BigDecimal.class), eq(1)))
                .thenReturn(new BigDecimal("100.00"));


        ShoppingCartPricingServiceV2 sut = new ShoppingCartPricingServiceV2(mockPricing);

        BigDecimal result = sut.computeLineTotal(new BigDecimal("50.0"), 1);

        assertEquals(new BigDecimal("100.00"), result);


        verify(mockPricing, times(1))
                .calculatePriceQuantity(new BigDecimal("50.0"), 1);
    }

}