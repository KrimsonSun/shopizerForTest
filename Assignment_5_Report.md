# Assignment 5: Testable Design and Mocking

## Part 1: Testable Design (20 points)

### 1.1 Aspects and Goals of Testable Design
A testable design is one that allows individual components to be verified in isolation from their environment. The primary goals include:
*   **Isolation (Decoupling)**: Components should not depend on concrete implementations of external systems (databases, file systems, network). Instead, they should depend on abstractions (interfaces).
*   **Controllability**: The tester should be able to force the software into specific states or paths (e.g., simulating a network timeout or a specific database return value).
*   **Determinism**: A testable design ensures that given the same input and environment state, the component produces the same output every time.
*   **Observability**: The internal state or outputs of a component should be easily accessible for verification.

### 1.2 Stubbing Implementation

**Existing Use of Stubbing:**
In the refactored `IntegrationModulesLoader`, we introduced the `IntegrationModuleSource` interface. 
*   **Usage**: The system now uses this interface to load raw data instead of directly accessing the classpath resources.
*   **Rationale**: This is used because the original implementation was tightly coupled to the Java ClassLoader and resource files. By stubbing this source, we can return pre-defined JSON strings in memory, making the tests fast and independent of the physical disk.

**[IMAGE PLACEHOLDER 1]**  
*Description: Screenshot showing the `IntegrationModuleSource` interface and its default implementation in `IntegrationModulesLoader.java`.*

**New Stub Implementation:**
I implemented `StubIntegrationModuleSource` inside `IntegrationModulesLoaderTest.java`.
*   **Technique**: I created a static inner class that implements the `IntegrationModuleSource` interface. 
*   **Test Case**: In `testLoadModulesWithValidJson`, this stub is injected into the loader. It returns a hardcoded JSON string, allowing us to verify the parser's logic without ever reading a real file.

**[IMAGE PLACEHOLDER 2]**  
*Description: Screenshot of the `StubIntegrationModuleSource` class and the test case using it.*

### 1.3 Analysis of Bad Testable Design

**Documented Code (Original Design):**
The original `IntegrationModulesLoader.loadIntegrationModules` method contained the following logic:
```java
InputStream in = this.getClass().getClassLoader().getResourceAsStream(jsonFilePath);
Map[] objects = mapper.readValue(in, Map[].class);
```
**The Problem**:
This design makes testing difficult because:
1.  **File System Dependency**: You cannot test how the code handles different JSON structures without creating multiple physical files in the `src/main/resources` folder.
2.  **Error Handling**: It is nearly impossible to simulate an `InputStream` failure or a specific I/O error without complex environment manipulation.
3.  **Side Effects**: Tests might accidentally overwrite or depend on shared resource files, leading to flaky tests.

**Advice for Fix**:
Replace the hardcoded instantiation/access with **Dependency Injection (DI)**. Define an interface for the resource loading behavior and pass that interface into the constructor.

**Implementation of New Design**:
I updated `IntegrationModulesLoader` to accept two interfaces: `IntegrationModuleSource` (for getting the string) and `IntegrationModuleParser` (for converting data to objects).

**[IMAGE PLACEHOLDER 3]**  
*Description: Screenshot of the refactored `IntegrationModulesLoader` constructor showing Dependency Injection.*

---

## Part 2: Mocking (20 points)

### 2.1 Mocking and its Utility
Mocking involves creating objects that simulate the behavior of real, complex objects. Its primary utilities are:
*   **Verification of Interactions**: Unlike stubs (which just provide data), mocks allow you to verify if a method was called, with what arguments, and how many times.
*   **Avoiding Side Effects**: Mocking an `EmailService` ensures you don't actually send 1,000 emails during a test run.
*   **Simulating External Systems**: Mocks can easily simulate external API failures or specific sequence of calls that are hard to trigger with real systems.

### 2.2 Feature for Mocking: Email Notification
The `EmailService` is a perfect candidate for mocking. In most enterprise applications, sending an email involves an SMTP server and network connectivity.
*   **Behavior Checking**: Without mocking, we could only check if the code runs without crashing. With Mockito mocking, we can check if the **correct recipient** was set and if the **Email Template Tokens** (like order ID and amount) were populated correctly.

**[IMAGE PLACEHOLDER 4]**  
*Description: Screenshot of the `EmailService` interface definition.*

### 2.3 Mockito Test Case
I implemented `EmailServiceMockTest.java` using Mockito.
*   **Key Technique**: Used `@Mock` for `EmailService` and `ArgumentCaptor` to inspect the `Email` object passed to the service.
*   **Verification**: The test `testOrderConfirmationEmailContentIsCorrect` captures the `Email` object and asserts that the subject and template tokens match the test data.

**[IMAGE PLACEHOLDER 5]**  
*Description: Screenshot of the JUnit test using `ArgumentCaptor` and `verify(mockEmailService).sendHtmlEmail(...)`.*

---

### Conclusion
By refactoring the code to use interfaces and dependency injection, we transformed a legacy "untestable" component into a modular service. Using Mockito allowed us to verify business logic (like email generation) without the overhead or risk of sending real emails.
