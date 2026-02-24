package com.salesmanager.test.business.loader;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import java.util.ArrayList;
import java.util.List;

import org.junit.Test;

import com.salesmanager.core.business.exception.ServiceException;
import com.salesmanager.core.business.services.reference.loader.IntegrationModulesLoader;
import com.salesmanager.core.model.system.IntegrationModule;

/**
 * Test case demonstrating improved testable design
 * Using dependency injection and mocking/stubbing
 * 
 * This test demonstrates:
 * 1. How to stub IntegrationModuleSource to return different JSON content
 * 2. How to mock IntegrationModuleParser for behavior verification
 * 3. How to test error handling without external dependencies
 * 4. How dependency injection makes testing easier
 */
public class IntegrationModulesLoaderTest {
    
    /**
     * Stub implementation of IntegrationModuleSource for testing
     * This demonstrates how to create a test double without external file I/O
     */
    static class StubIntegrationModuleSource implements IntegrationModuleSource {
        private String jsonToReturn;
        private boolean throwException;
        private String exceptionMessage;
        
        public StubIntegrationModuleSource(String jsonToReturn) {
            this.jsonToReturn = jsonToReturn;
            this.throwException = false;
            this.exceptionMessage = "Stubbed exception: file not found";
        }
        
        public void setThrowException(boolean throwException) {
            this.throwException = throwException;
        }
        
        public void setExceptionMessage(String msg) {
            this.exceptionMessage = msg;
        }
        
        @Override
        public String loadRawJson(String identifier) throws ServiceException {
            if (throwException) {
                throw new ServiceException(exceptionMessage);
            }
            return jsonToReturn;
        }
    }
    
    /**
     * Test 1: Load modules with valid JSON
     * Demonstrates: Basic mock setup and verification
     */
    @Test
    public void testLoadModulesWithValidJson() throws Exception {
        // Arrange: Create stub that returns valid JSON
        String validJson = "[{" +
            "\"module\": \"payment\", " +
            "\"code\": \"paypal\", " +
            "\"image\": \"paypal.png\"" +
            "}]";
        
        IntegrationModuleSource stubSource = new StubIntegrationModuleSource(validJson);
        IntegrationModuleParser mockParser = mock(IntegrationModuleParser.class);
        
        // Setup mock parser to return modules
        List<IntegrationModule> expectedModules = new ArrayList<>();
        IntegrationModule module = new IntegrationModule();
        module.setCode("paypal");
        expectedModules.add(module);
        
        when(mockParser.parseModules(validJson)).thenReturn(expectedModules);
        
        // Act: Create loader with injected stub and mock
        IntegrationModulesLoader loader = new IntegrationModulesLoader(
            stubSource, mockParser);
        List<IntegrationModule> result = loader.loadIntegrationModules("data/modules.json");
        
        // Assert
        assertNotNull("Result should not be null", result);
        assertEquals("Should have 1 module", 1, result.size());
        assertEquals("Module code should be paypal", "paypal", result.get(0).getCode());
        
        // Verify the parser was called with the JSON content
        verify(mockParser).parseModules(validJson);
    }
    
    /**
     * Test 2: Handle source exception
     * Demonstrates: Exception stubbing
     */
    @Test
    public void testLoadModulesWithSourceException() throws Exception {
        // Arrange: Create stub that throws exception
        StubIntegrationModuleSource stubSource = new StubIntegrationModuleSource("");
        stubSource.setThrowException(true);
        stubSource.setExceptionMessage("Stubbed exception: file not found");
        
        IntegrationModuleParser mockParser = mock(IntegrationModuleParser.class);
        
        // Act & Assert
        IntegrationModulesLoader loader = new IntegrationModulesLoader(
            stubSource, mockParser);
        
        ServiceException exception = assertThrows(ServiceException.class, () -> {
            loader.loadIntegrationModules("nonexistent.json");
        });
        
        // Verify exception message
        assertTrue("Exception should mention file not found", 
            exception.getMessage().contains("file not found"));
    }
    
    /**
     * Test 3: Handle parsing error
     * Demonstrates: Mock throwing exceptions
     */
    @Test
    public void testLoadModulesWithParsingError() throws Exception {
        // Arrange: Valid source but parser fails
        String validJson = "[invalid json]";
        IntegrationModuleSource validSource = new StubIntegrationModuleSource(validJson);
        
        IntegrationModuleParser mockParser = mock(IntegrationModuleParser.class);
        when(mockParser.parseModules(validJson))
            .thenThrow(new ServiceException("Parse error"));
        
        // Act & Assert
        IntegrationModulesLoader loader = new IntegrationModulesLoader(
            validSource, mockParser);
        
        ServiceException exception = assertThrows(ServiceException.class, () -> {
            loader.loadIntegrationModules("data/modules.json");
        });
        
        assertTrue("Exception should mention parse error", 
            exception.getMessage().contains("Parse error"));
    }
    
    /**
     * Test 4: Test with different JSON sources
     * Demonstrates: Benefits of dependency injection - easy to swap implementations
     */
    @Test
    public void testLoaderWithDifferentSources() throws Exception {
        // Source 1: Returns modules
        IntegrationModuleSource source1 = new StubIntegrationModuleSource(
            "[{\"module\": \"payment\", \"code\": \"stripe\", \"image\": \"stripe.png\"}]");
        
        // Source 2: Returns empty list
        IntegrationModuleSource source2 = new StubIntegrationModuleSource("[]");
        
        IntegrationModuleParser mockParser = mock(IntegrationModuleParser.class);
        when(mockParser.parseModules(anyString()))
            .thenReturn(new ArrayList<>());
        
        // Each loader uses different source - all testable without file system
        IntegrationModulesLoader loader1 = new IntegrationModulesLoader(source1, mockParser);
        IntegrationModulesLoader loader2 = new IntegrationModulesLoader(source2, mockParser);
        
        // Both work seamlessly - this would be impossible with the old design
        assertNotNull("Loader 1 should work", loader1.loadIntegrationModules("modules.json"));
        assertNotNull("Loader 2 should work", loader2.loadIntegrationModules("modules.json"));
    }
    
    /**
     * Interface for module source - demonstrates improved design
     * This would be extracted to a separate file in real implementation
     */
    public interface IntegrationModuleSource {
        String loadRawJson(String identifier) throws ServiceException;
    }
    
    /**
     * Interface for module parser - demonstrates separation of concerns
     * This would be extracted to a separate file in real implementation
     */
    public interface IntegrationModuleParser {
        List<IntegrationModule> parseModules(String jsonContent) throws ServiceException;
    }
}
