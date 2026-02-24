package com.salesmanager.test.business.services;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.ArgumentCaptor;

import com.salesmanager.core.business.exception.ServiceException;
import com.salesmanager.core.business.services.system.EmailService;
import com.salesmanager.core.model.merchant.MerchantStore;

/**
 * Mocking EmailService to verify email behavior without sending real emails
 * 
 * Demonstrates advanced Mockito features:
 * - Creating and injecting mocks
 * - Verifying method calls with specific arguments
 * - Capturing arguments for detailed verification
 * - Testing exception handling with mocks
 * - Testing conditional logic based on mock behavior
 * 
 * Key Learning Points:
 * 1. Tests run instantly without SMTP calls
 * 2. Can verify exact parameters passed to external services
 * 3. Can simulate failures to test error handling
 * 4. Can test behavior without side effects
 */
public class EmailServiceMockTest {
    
    /**
     * Example service that uses EmailService
     * In real code, this would be OrderService, CustomerService, etc.
     * This demonstrates why mocking external services is important.
     */
    static class OrderNotificationService {
        private EmailService emailService;
        
        public OrderNotificationService(EmailService emailService) {
            this.emailService = emailService;
        }
        
        /**
         * Send order confirmation email
         * This is the method we want to test without actually sending email
         */
        public void sendOrderConfirmation(String customerEmail, String orderId, 
                double totalAmount, MerchantStore store) throws ServiceException {
            
            // Validate inputs
            if (customerEmail == null || customerEmail.isEmpty()) {
                throw new ServiceException("Customer email is required");
            }
            if (totalAmount <= 0) {
                throw new ServiceException("Order amount must be positive");
            }
            
            // Build email content
            String subject = "Order Confirmation: " + orderId;
            String body = String.format(
                "Thank you for your order!\n" +
                "Order ID: %s\n" +
                "Total: $%.2f\n" +
                "Store: %s\n",
                orderId, totalAmount, store.getStorename());
            
            // Send email - this is what we'll mock
            emailService.sendHtmlEmail(store, customerEmail, null, subject, body, null);
        }
        
        /**
         * Send email to admin when high-value order received
         * This demonstrates testing conditional behavior
         */
        public void notifyAdminHighValueOrder(String adminEmail, String orderId, 
                double totalAmount) throws ServiceException {
            
            if (totalAmount > 10000) {
                String subject = "High-value order alert: " + orderId;
                String body = String.format(
                    "An order for $%.2f has been placed (Order ID: %s)\n" +
                    "This exceeds the $10,000 threshold.",
                    totalAmount, orderId);
                
                emailService.sendHtmlEmail(null, adminEmail, null, subject, body, null);
            }
        }
    }
    
    // Mocked dependencies
    @Mock
    private EmailService mockEmailService;
    
    @Mock
    private MerchantStore mockStore;
    
    private OrderNotificationService notificationService;
    
    @Before
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        notificationService = new OrderNotificationService(mockEmailService);
        
        // Setup mock store
        when(mockStore.getStorename()).thenReturn("Test Store");
    }
    
    /**
     * Test 1: Verify email is called with correct parameters
     * DEMONSTRATES: Basic mock verification and call counting
     */
    @Test
    public void testOrderConfirmationEmailIsSent() throws ServiceException {
        // Arrange
        String customerEmail = "customer@example.com";
        String orderId = "ORD-12345";
        double totalAmount = 99.99;
        
        // Act: Send order confirmation
        notificationService.sendOrderConfirmation(
            customerEmail, orderId, totalAmount, mockStore);
        
        // Assert: Verify EmailService was called exactly once
        verify(mockEmailService, times(1)).sendHtmlEmail(
            any(MerchantStore.class),
            eq(customerEmail),
            isNull(),
            contains("ORD-12345"),
            contains("99.99"),
            isNull()
        );
    }
    
    /**
     * Test 2: Capture and verify email content details
     * DEMONSTRATES: ArgumentCaptor for detailed assertions on call arguments
     */
    @Test
    public void testOrderConfirmationEmailContentIsCorrect() throws ServiceException {
        // Arrange
        String customerEmail = "john@example.com";
        String orderId = "ORD-67890";
        double totalAmount = 299.50;
        
        ArgumentCaptor<String> subjectCaptor = ArgumentCaptor.forClass(String.class);
        ArgumentCaptor<String> bodyCaptor = ArgumentCaptor.forClass(String.class);
        
        // Act
        notificationService.sendOrderConfirmation(
            customerEmail, orderId, totalAmount, mockStore);
        
        // Assert: Capture the arguments passed to sendHtmlEmail
        verify(mockEmailService).sendHtmlEmail(
            any(MerchantStore.class),
            eq(customerEmail),
            isNull(),
            subjectCaptor.capture(),
            bodyCaptor.capture(),
            isNull()
        );
        
        // Verify email subject and body content
        String subject = subjectCaptor.getValue();
        String body = bodyCaptor.getValue();
        
        assertTrue("Subject should contain order ID", 
            subject.contains("ORD-67890"));
        assertTrue("Subject should contain 'Confirmation'", 
            subject.contains("Confirmation"));
        assertTrue("Body should contain order ID", 
            body.contains("ORD-67890"));
        assertTrue("Body should contain amount", 
            body.contains("299.50"));
        assertTrue("Body should contain store name", 
            body.contains("Test Store"));
    }
    
    /**
     * Test 3: Verify email is NOT sent for invalid inputs
     * DEMONSTRATES: Negative testing - verifying things DON'T happen
     */
    @Test
    public void testOrderConfirmationThrowsExceptionForEmptyEmail() {
        // Arrange: Empty customer email
        String customerEmail = "";
        
        // Act & Assert: Exception should be thrown
        assertThrows(ServiceException.class, () -> {
            notificationService.sendOrderConfirmation(
                customerEmail, "ORD-111", 50.0, mockStore);
        });
        
        // Verify: Email service should NOT be called
        verify(mockEmailService, never()).sendHtmlEmail(any(), any(), any(), any(), any(), any());
    }
    
    /**
     * Test 4: Verify email is NOT sent for zero/negative amounts
     * DEMONSTRATES: Input validation testing
     */
    @Test
    public void testOrderConfirmationThrowsExceptionForNegativeAmount() {
        // Act & Assert: Negative amount should throw exception
        assertThrows(ServiceException.class, () -> {
            notificationService.sendOrderConfirmation(
                "customer@example.com", "ORD-222", -50.0, mockStore);
        });
        
        // Verify: Email service not called for invalid input
        verify(mockEmailService, never()).sendHtmlEmail(any(), any(), any(), any(), any(), any());
    }
    
    /**
     * Test 5: Simulate email service failure
     * DEMONSTRATES: Testing error handling with mock exceptions
     * This shows the key advantage of mocking: test failures without real consequences
     */
    @Test
    public void testOrderConfirmationHandlesEmailException() throws ServiceException {
        // Arrange: Mock email service to throw exception
        doThrow(new ServiceException("SMTP server unreachable"))
            .when(mockEmailService)
            .sendHtmlEmail(any(), any(), any(), any(), any(), any());
        
        // Act & Assert: Service should propagate email exception
        ServiceException exception = assertThrows(ServiceException.class, () -> {
            notificationService.sendOrderConfirmation(
                "customer@example.com", "ORD-333", 75.0, mockStore);
        });
        
        // Verify exception contains email service error
        assertTrue("Exception should mention SMTP", 
            exception.getMessage().contains("SMTP"));
    }
    
    /**
     * Test 6: Verify high-value order notification logic
     * DEMONSTRATES: Testing conditional behavior with mocks
     */
    @Test
    public void testAdminNotificationSentForHighValueOrder() throws ServiceException {
        // Arrange
        String adminEmail = "admin@store.com";
        double highValue = 15000.0;
        
        // Act: Notify admin of high-value order
        notificationService.notifyAdminHighValueOrder(adminEmail, "ORD-999", highValue);
        
        // Assert: Admin notification should be sent
        verify(mockEmailService, times(1)).sendHtmlEmail(
            isNull(),
            eq(adminEmail),
            isNull(),
            contains("High-value order"),
            contains("15000"),
            isNull()
        );
    }
    
    /**
     * Test 7: Verify admin notification NOT sent for normal orders
     * DEMONSTRATES: Boundary testing with mocks
     */
    @Test
    public void testAdminNotificationNotSentForNormalOrder() throws ServiceException {
        // Arrange
        String adminEmail = "admin@store.com";
        double normalValue = 5000.0;  // Below 10000 threshold
        
        // Act: Notify admin (but shouldn't send for normal order)
        notificationService.notifyAdminHighValueOrder(adminEmail, "ORD-low", normalValue);
        
        // Assert: No email should be sent
        verify(mockEmailService, never()).sendHtmlEmail(any(), any(), any(), any(), any(), any());
    }
    
    /**
     * Test 8: Verify email sent for order exactly at high-value threshold
     * DEMONSTRATES: Boundary value analysis
     */
    @Test
    public void testAdminNotificationForOrderAtThreshold() throws ServiceException {
        // Arrange: Order amount = exactly at $10,000 threshold
        String adminEmail = "admin@store.com";
        double atThreshold = 10000.0;
        
        // Act
        notificationService.notifyAdminHighValueOrder(adminEmail, "ORD-threshold", atThreshold);
        
        // Assert: No email (threshold check is > 10000, not >= 10000)
        verify(mockEmailService, never()).sendHtmlEmail(any(), any(), any(), any(), any(), any());
        
        // But one cent more should send
        notificationService.notifyAdminHighValueOrder(adminEmail, "ORD-over", 10000.01);
        verify(mockEmailService, times(1)).sendHtmlEmail(any(), any(), any(), any(), any(), any());
    }
    
    /**
     * Test 9: Verify multiple emails in sequence
     * DEMONSTRATES: Verifying multiple calls with verify() count
     */
    @Test
    public void testMultipleOrderConfirmationsInSequence() throws ServiceException {
        // Arrange
        String email1 = "customer1@example.com";
        String email2 = "customer2@example.com";
        
        // Act: Send two confirmations
        notificationService.sendOrderConfirmation(email1, "ORD-001", 50.0, mockStore);
        notificationService.sendOrderConfirmation(email2, "ORD-002", 75.0, mockStore);
        
        // Assert: Email service should be called twice
        verify(mockEmailService, times(2)).sendHtmlEmail(
            any(MerchantStore.class),
            anyString(),
            isNull(),
            anyString(),
            anyString(),
            isNull()
        );
        
        // Verify specific calls
        verify(mockEmailService).sendHtmlEmail(any(), eq(email1), any(), any(), any(), any());
        verify(mockEmailService).sendHtmlEmail(any(), eq(email2), any(), any(), any(), any());
    }
}
