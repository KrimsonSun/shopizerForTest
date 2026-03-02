package com.salesmanager.test.shoppingcart;

import com.salesmanager.core.model.common.UserContext;

public interface UserContextProvider {
    String getIpAddressOrNull();
}