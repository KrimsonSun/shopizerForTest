#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

def add_heading_style(doc, text, level):
    """Add a heading with appropriate styling"""
    heading = doc.add_heading(text, level=level)
    return heading

def add_paragraph_spacing(paragraph, space_before=12, space_after=12):
    """Add spacing to paragraph"""
    paragraph.paragraph_format.space_before = Pt(space_before)
    paragraph.paragraph_format.space_after = Pt(space_after)

def shade_cell(cell, color):
    """Shade a table cell"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color)
    cell._element.get_or_add_tcPr().append(shading_elm)

def create_test_report():
    """Generate comprehensive test report for Shopizer"""
    doc = Document()
    
    # Title Page
    title = doc.add_heading('Shopizer E-Commerce Platform', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle = doc.add_paragraph('Comprehensive Testing and Partitioning Analysis Report')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_font = subtitle.runs[0].font
    subtitle_font.size = Pt(14)
    subtitle_font.italic = True
    
    date_para = doc.add_paragraph(f'Report Date: {datetime.date.today().strftime("%B %d, %Y")}')
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()  # Blank line
    
    # Table of Contents
    add_heading_style(doc, 'Table of Contents', 1)
    toc_items = [
        '1. Introduction',
        '2. Project Overview',
        '3. Build and Deployment',
        '4. Existing Test Framework',
        '5. Systematic Functional Testing & Partition Testing',
        '6. Product Service: Partition-Based Test Design',
        '7. Test Implementation and Results',
        '8. Conclusion',
    ]
    for item in toc_items:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_page_break()
    
    # 1. Introduction
    add_heading_style(doc, '1. Introduction', 1)
    intro = doc.add_paragraph(
        'Shopizer is an open-source, enterprise-grade e-commerce platform designed to '
        'provide a headless, REST API-based commerce solution. This report documents a '
        'comprehensive analysis of the Shopizer codebase, focusing on its existing testing '
        'infrastructure and the development of systematic partition-based test cases. '
        'The analysis includes project metrics, build procedures, existing test frameworks, '
        'and the design and implementation of new test cases using partition testing methodology.'
    )
    add_paragraph_spacing(intro)
    
    # 2. Project Overview
    add_heading_style(doc, '2. Project Overview', 1)
    
    add_heading_style(doc, '2.1 Project Description', 2)
    desc = doc.add_paragraph(
        'Shopizer is a Java-based open-source e-commerce platform that provides a complete '
        'headless commerce solution. The platform is modular and designed to support various '
        'e-commerce requirements including product catalog management, shopping cart, checkout, '
        'order management, customer management, and payment processing.'
    )
    add_paragraph_spacing(desc)
    
    add_heading_style(doc, '2.2 Key Features', 2)
    features = [
        'Headless REST API architecture',
        'Multi-merchant support',
        'Product catalog with categories and attributes',
        'Shopping cart and checkout management',
        'Order processing and tracking',
        'Customer account management',
        'Payment gateway integration',
        'Search and filtering capabilities',
        'Content management system',
    ]
    for feature in features:
        doc.add_paragraph(feature, style='List Bullet')
    
    add_heading_style(doc, '2.3 Technology Stack', 2)
    
    # Technology table
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Component'
    hdr_cells[1].text = 'Technology'
    shade_cell(hdr_cells[0], 'D3D3D3')
    shade_cell(hdr_cells[1], 'D3D3D3')
    
    tech_data = [
        ('Language', 'Java 11, 17'),
        ('Framework', 'Spring Boot 2.x'),
        ('ORM', 'Hibernate 5.x'),
        ('Database', 'PostgreSQL, MySQL, H2'),
        ('Build Tool', 'Maven 3.6+'),
        ('API Documentation', 'Swagger/SpringFox'),
        ('Testing Framework', 'JUnit 4.x, Mockito'),
        ('Container', 'Docker'),
    ]
    for component, tech in tech_data:
        row_cells = table.add_row().cells
        row_cells[0].text = component
        row_cells[1].text = tech
    
    add_heading_style(doc, '2.4 Project Metrics', 2)
    
    metrics_para = doc.add_paragraph()
    metrics_para.add_run('Total Java Files: ').bold = True
    metrics_para.add_run('1,210\n')
    metrics_para.add_run('Total Lines of Code (LOC): ').bold = True
    metrics_para.add_run('115,093\n')
    metrics_para.add_run('Average LOC per File: ').bold = True
    metrics_para.add_run('~95 lines\n')
    metrics_para.add_run('Number of Modules: ').bold = True
    metrics_para.add_run('5 (sm-core, sm-core-model, sm-core-modules, sm-shop, sm-shop-model)\n')
    
    # 3. Build and Deployment
    doc.add_page_break()
    add_heading_style(doc, '3. Build and Deployment', 1)
    
    add_heading_style(doc, '3.1 Prerequisites', 2)
    doc.add_paragraph('Java Development Kit (JDK) 11 or 17', style='List Bullet')
    doc.add_paragraph('Maven 3.6 or higher', style='List Bullet')
    doc.add_paragraph('Git', style='List Bullet')
    doc.add_paragraph('Docker (optional, for containerized deployment)', style='List Bullet')
    doc.add_paragraph('PostgreSQL or MySQL (optional, for production database)', style='List Bullet')
    
    add_heading_style(doc, '3.2 Build Process', 2)
    build_steps = doc.add_paragraph()
    build_steps.add_run('Step 1: Clone Repository\n').bold = True
    build_steps.add_run('git clone https://github.com/shopizer-ecommerce/shopizer.git\n\n')
    build_steps.add_run('Step 2: Build with Maven\n').bold = True
    build_steps.add_run('cd shopizer\nmvnw clean install\n\n')
    build_steps.add_run('Step 3: Run Tests\n').bold = True
    build_steps.add_run('mvnw test\n\n')
    build_steps.add_run('Step 4: Build Backend JAR\n').bold = True
    build_steps.add_run('cd sm-shop\nmvnw spring-boot:run\n\n')
    
    add_heading_style(doc, '3.3 Docker Deployment', 2)
    docker_para = doc.add_paragraph(
        'A complete docker-compose configuration has been created to support deployment with PostgreSQL. '
        'This configuration includes:'
    )
    doc.add_paragraph('PostgreSQL database container (port 5432)', style='List Bullet')
    doc.add_paragraph('Shopizer backend API (port 8080)', style='List Bullet')
    doc.add_paragraph('Shopizer admin UI (port 82)', style='List Bullet')
    doc.add_paragraph('Shopizer shop React frontend (port 80)', style='List Bullet')
    
    deploy_cmd = doc.add_paragraph()
    deploy_cmd.add_run('Deployment Command:\n').bold = True
    deploy_cmd.add_run('docker-compose up -d')
    
    # 4. Existing Test Framework
    doc.add_page_break()
    add_heading_style(doc, '4. Existing Test Framework', 1)
    
    add_heading_style(doc, '4.1 Testing Infrastructure', 2)
    framework_para = doc.add_paragraph(
        'Shopizer uses JUnit 4 as its primary testing framework with Mockito for mocking dependencies. '
        'The project contains approximately 20+ test classes distributed across core business logic, '
        'catalog operations, order management, shipping calculations, and customer management.'
    )
    add_paragraph_spacing(framework_para)
    
    add_heading_style(doc, '4.2 Test Organization', 2)
    test_structure = doc.add_paragraph()
    test_structure.add_run('Test Location: ').bold = True
    test_structure.add_run('src/test/java/com/salesmanager/test/\n\n')
    test_structure.add_run('Key Test Classes:\n')
    
    test_classes = [
        'ProductTest.java - Tests for product catalog operations',
        'CategoryTest.java - Tests for category management',
        'OrderTest.java - Tests for order processing',
        'CustomerTest.java - Tests for customer operations',
        'ShoppingCartTest.java - Tests for shopping cart functionality',
        'ShippingMethodDecisionTest.java - Tests for shipping calculations',
        'PaymentTest.java - Tests for payment processing',
        'ContentFolderTest.java - Tests for content management',
    ]
    for test_class in test_classes:
        doc.add_paragraph(test_class, style='List Bullet')
    
    add_heading_style(doc, '4.3 Base Test Class', 2)
    base_para = doc.add_paragraph(
        'All test classes extend AbstractSalesManagerCoreTestCase, which provides:'
    )
    doc.add_paragraph('Spring application context initialization', style='List Bullet')
    doc.add_paragraph('Transaction management and rollback', style='List Bullet')
    doc.add_paragraph('Access to service beans (ProductService, CategoryService, etc.)', style='List Bullet')
    doc.add_paragraph('Database initialization and cleanup', style='List Bullet')
    
    add_heading_style(doc, '4.4 How to Run Tests', 2)
    run_tests = doc.add_paragraph()
    run_tests.add_run('Run all tests:\n').bold = True
    run_tests.add_run('mvnw test\n\n')
    run_tests.add_run('Run specific test class:\n').bold = True
    run_tests.add_run('mvnw test -Dtest=ProductTest\n\n')
    run_tests.add_run('Run specific test method:\n').bold = True
    run_tests.add_run('mvnw test -Dtest=ProductTest#testCreateProduct\n\n')
    run_tests.add_run('Run with detailed logging:\n').bold = True
    run_tests.add_run('mvnw test -X\n')
    
    # 5. Systematic Functional Testing & Partition Testing
    doc.add_page_break()
    add_heading_style(doc, '5. Systematic Functional Testing & Partition Testing', 1)
    
    add_heading_style(doc, '5.1 Motivation for Systematic Testing', 2)
    motivation = doc.add_paragraph(
        'Complex software systems like e-commerce platforms require systematic and thorough testing '
        'to ensure reliability, correctness, and maintainability. A comprehensive test strategy must address '
        'the following challenges:'
    )
    doc.add_paragraph(
        'Input Space: E-commerce systems accept diverse inputs with varying characteristics, '
        'making exhaustive testing infeasible.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Business Logic Complexity: Multiple interdependent operations (catalog, cart, orders) '
        'create complex interactions requiring focused testing.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Error Handling: Systems must gracefully handle invalid inputs, edge cases, and '
        'resource constraints.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Regression Prevention: Test suites must detect unintended changes to existing functionality.',
        style='List Bullet'
    )
    
    add_heading_style(doc, '5.2 Partition Testing Methodology', 2)
    partition_def = doc.add_paragraph(
        'Partition testing, also known as equivalence class partitioning, is a black-box testing '
        'technique that divides the input domain into subsets (equivalence classes) where all inputs '
        'within a partition are expected to behave similarly. This approach:'
    )
    doc.add_paragraph(
        'Reduces test cases: Instead of testing all possible inputs, representative values from '
        'each partition are tested.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Improves coverage: Systematic partitioning ensures all meaningful input combinations are addressed.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Identifies boundaries: Boundary value analysis within partitions reveals edge cases and off-by-one errors.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Enhances maintainability: Clear partitioning makes test rationale transparent and test suites easier to maintain.',
        style='List Bullet'
    )
    
    # 6. Product Service: Partition-Based Test Design
    doc.add_page_break()
    add_heading_style(doc, '6. Product Service: Partition-Based Test Design', 1)
    
    add_heading_style(doc, '6.1 Selected Feature: Product Creation and Validation', 2)
    feature_desc = doc.add_paragraph(
        'The Product Service is a critical component of the Shopizer catalog system. '
        'Product creation and validation represents a complex feature with multiple input parameters '
        'and business constraints, making it an ideal candidate for partition-based testing. '
        'This service validates product attributes, pricing, inventory, and relationships.'
    )
    add_paragraph_spacing(feature_desc)
    
    add_heading_style(doc, '6.2 Partitioning Scheme: Product Price Validation', 2)
    partition_rationale = doc.add_paragraph(
        'We selected product price validation as the focus for partition testing. '
        'Price is a fundamental e-commerce attribute with specific business constraints: '
        'prices must be non-negative, reasonably bounded, and precise to monetary units.'
    )
    add_paragraph_spacing(partition_rationale)
    
    add_heading_style(doc, '6.3 Partition Definition', 2)
    
    partition_table = doc.add_table(rows=1, cols=4)
    partition_table.style = 'Light Grid Accent 1'
    hdr_cells = partition_table.rows[0].cells
    hdr_cells[0].text = 'Partition'
    hdr_cells[1].text = 'Description'
    hdr_cells[2].text = 'Valid Range'
    hdr_cells[3].text = 'Representative Value'
    for cell in hdr_cells:
        shade_cell(cell, 'D3D3D3')
    
    partitions_data = [
        ('Zero Price', 'Products offered for free', '0.00', '0.00'),
        ('Normal Price', 'Standard product pricing', '0.01 - 999,999.99', '29.99'),
        ('High Price', 'Premium products', '1,000.00 - 9,999.99', '1,499.99'),
        ('Premium Price', 'Luxury items', '10,000.00+', '15,000.00'),
        ('Invalid: Negative', 'Negative prices (invalid)', '< 0', '-10.00'),
        ('Invalid: Decimal', 'Non-monetary precision', 'More than 2 decimals', '29.999'),
        ('Invalid: Null', 'Missing price', 'null', 'null'),
    ]
    
    for partition, description, range_val, representative in partitions_data:
        row_cells = partition_table.add_row().cells
        row_cells[0].text = partition
        row_cells[1].text = description
        row_cells[2].text = range_val
        row_cells[3].text = representative
    
    add_heading_style(doc, '6.4 Boundary Value Analysis', 2)
    
    boundary_table = doc.add_table(rows=1, cols=3)
    boundary_table.style = 'Light Grid Accent 1'
    hdr_cells = boundary_table.rows[0].cells
    hdr_cells[0].text = 'Boundary'
    hdr_cells[1].text = 'Value'
    hdr_cells[2].text = 'Expected Result'
    for cell in hdr_cells:
        shade_cell(cell, 'D3D3D3')
    
    boundaries = [
        ('Lower Valid', '0.00', 'ACCEPT'),
        ('First Invalid Below', '-0.01', 'REJECT'),
        ('Decimal Lower', '0.01', 'ACCEPT'),
        ('Decimal Upper', '999,999.99', 'ACCEPT'),
        ('High Precision', '0.001', 'REJECT'),
        ('Upper Boundary', '9,999,999.99', 'ACCEPT'),
    ]
    
    for boundary, value, result in boundaries:
        row_cells = boundary_table.add_row().cells
        row_cells[0].text = boundary
        row_cells[1].text = value
        row_cells[2].text = result
    
    # 7. Test Implementation
    doc.add_page_break()
    add_heading_style(doc, '7. Test Implementation and Results', 1)
    
    add_heading_style(doc, '7.1 New JUnit Test Cases', 2)
    test_impl = doc.add_paragraph(
        'The following JUnit test class implements comprehensive partition-based testing for the '
        'ProductService price validation feature. Each test method corresponds to a specific partition '
        'and validates the service behavior against the expected outcome.'
    )
    add_paragraph_spacing(test_impl)
    
    add_heading_style(doc, '7.2 Test Class: ProductPricePartitionTest.java', 2)
    
    # Create code example box
    code_box = doc.add_paragraph()
    code_box.add_run('File Location: ').bold = True
    code_box.add_run('sm-core/src/test/java/com/salesmanager/test/catalog/ProductPricePartitionTest.java')
    
    doc.add_paragraph()
    code_para = doc.add_paragraph(
        'package com.salesmanager.test.catalog;\n\n'
        'import java.math.BigDecimal;\n'
        'import org.junit.Test;\n'
        'import org.junit.Assert;\n'
        'import com.salesmanager.core.business.exception.ServiceException;\n'
        'import com.salesmanager.core.model.catalog.product.Product;\n'
        'import com.salesmanager.core.model.catalog.product.price.ProductPrice;\n'
        'import com.salesmanager.core.model.merchant.MerchantStore;\n'
        'import com.salesmanager.core.model.reference.language.Language;\n'
        '\n'
        'public class ProductPricePartitionTest extends AbstractSalesManagerCoreTestCase {\n'
        '    /**\n'
        '     * PARTITION 1: Zero Price\n'
        '     * Test product creation with zero price (free product)\n'
        '     * Expected: ACCEPT - Zero is a valid price for promotional products\n'
        '     */\n'
        '    @Test\n'
        '    public void testCreateProductWithZeroPrice() throws Exception {\n'
        '        BigDecimal zeroPrice = new BigDecimal("0.00");\n'
        '        Product product = createProductWithPrice(zeroPrice);\n'
        '        Assert.assertNotNull(product);\n'
        '        Assert.assertEquals(0, zeroPrice.compareTo(product.getPrice()));\n'
        '    }\n'
        '\n'
        '    /**\n'
        '     * PARTITION 2: Normal Price\n'
        '     * Test product with typical pricing ($29.99)\n'
        '     * Expected: ACCEPT - Within normal pricing range\n'
        '     */\n'
        '    @Test\n'
        '    public void testCreateProductWithNormalPrice() throws Exception {\n'
        '        BigDecimal normalPrice = new BigDecimal("29.99");\n'
        '        Product product = createProductWithPrice(normalPrice);\n'
        '        Assert.assertNotNull(product);\n'
        '        Assert.assertEquals(0, normalPrice.compareTo(product.getPrice()));\n'
        '    }\n'
        '}\n'
    )
    code_para_format = code_para.paragraph_format
    code_para_format.left_indent = Inches(0.5)
    code_para_format.right_indent = Inches(0.5)
    
    # 7.3 Test Cases and Results
    doc.add_page_break()
    add_heading_style(doc, '7.3 Test Cases and Actual Results', 2)
    
    test_results_intro = doc.add_paragraph(
        'Two comprehensive test suites were implemented and executed: ProductPricePartitionTest.java '
        'by Yijun Sun and MyCartQuantityTest.java by Yuqian Chiu. The following sections present '
        'all test cases organized by partition, along with their actual execution results.'
    )
    add_paragraph_spacing(test_results_intro)
    
    # Test 1: ProductPricePartitionTest (by Yijun Sun)
    add_heading_style(doc, '7.3.1 ProductPricePartitionTest (Author: Yijun Sun)', 3)
    
    author_para = doc.add_paragraph()
    author_para.add_run('Test Author: ').bold = True
    author_para.add_run('Yijun Sun')
    
    file_para = doc.add_paragraph()
    file_para.add_run('File Location: ').bold = True
    file_para.add_run('sm-core/src/test/java/com/salesmanager/test/catalog/ProductPricePartitionTest.java')
    
    exec_para = doc.add_paragraph()
    exec_para.add_run('Test Execution: ').bold = True
    exec_para.add_run('19 tests run, 14 passed, 5 failed (expected failures)')
    
    desc_para = doc.add_paragraph(
        'This test suite validates product price handling across 7 partitions covering valid prices, '
        'boundary values, and invalid inputs including negative prices, null values, and precision errors.'
    )
    add_paragraph_spacing(desc_para)
    
    # ProductPrice Test Results Table
    price_results_table = doc.add_table(rows=1, cols=5)
    price_results_table.style = 'Light Grid Accent 1'
    hdr_cells = price_results_table.rows[0].cells
    hdr_cells[0].text = 'Partition'
    hdr_cells[1].text = 'Test Method'
    hdr_cells[2].text = 'Price Value'
    hdr_cells[3].text = 'Expected'
    hdr_cells[4].text = 'Result'
    for cell in hdr_cells:
        shade_cell(cell, '4472C4')  # Blue header
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    # ProductPrice test cases
    price_test_cases = [
        ('Partition 1:\nSmall Amount\n(0.01-9.99)', 'testPartition1_SmallAmount_LowValue', '$0.01', 'PASS', '✅ PASS'),
        ('', 'testPartition1_SmallAmount_TypicalLow', '$1.00', 'PASS', '✅ PASS'),
        ('', 'testPartition1_SmallAmount_UpperBound', '$9.99', 'PASS', '✅ PASS'),
        
        ('Partition 2:\nMedium Amount\n(10-99.99)', 'testPartition2_MediumAmount_LowerBound', '$10.00', 'PASS', '✅ PASS'),
        ('', 'testPartition2_MediumAmount_Typical', '$50.00', 'PASS', '✅ PASS'),
        ('', 'testPartition2_MediumAmount_UpperBound', '$99.99', 'PASS', '✅ PASS'),
        
        ('Partition 3:\nLarge Amount\n(100-999.99)', 'testPartition3_LargeAmount_LowerBound', '$100.00', 'PASS', '✅ PASS'),
        ('', 'testPartition3_LargeAmount_Typical', '$500.00', 'PASS', '✅ PASS'),
        ('', 'testPartition3_LargeAmount_UpperBound', '$999.99', 'PASS', '✅ PASS'),
        
        ('Partition 4:\nVery Large\n(≥1000)', 'testPartition4_VeryLargeAmount_LowerBound', '$1,000.00', 'PASS', '✅ PASS'),
        ('', 'testPartition4_VeryLargeAmount_Typical', '$5,000.00', 'PASS', '✅ PASS'),
        ('', 'testPartition4_VeryLargeAmount_Maximum', '$9,999.99', 'PASS', '✅ PASS'),
        
        ('Partition 5:\nBoundary Values', 'testPartition5_BoundaryZero_FreeProduct', '$0.00', 'PASS', '✅ PASS'),
        ('', 'testPartition5_BoundaryMaximum_PremiumProduct', '$10,000.00', 'PASS', '✅ PASS'),
        ('', 'testPartition5_InvalidNegativePrice', '-$10.00', 'REJECT', '❌ FAIL*'),
        ('', 'testPartition5_BoundaryNegative_JustBelowZero', '-$0.01', 'REJECT', '❌ FAIL*'),
        
        ('Partition 6:\nInvalid Precision', 'testPartition6_InvalidDecimalPrecision_ThreeDecimals', '$99.999', 'REJECT/ROUND', '❌ FAIL*'),
        ('', 'testPartition6_InvalidDecimalPrecision_ExtremeDecimals', '$99.123456', 'REJECT/ROUND', '❌ FAIL*'),
        
        ('Partition 7:\nNull/Invalid', 'testPartition7_InvalidNullPrice_HandlesGracefully', 'null', 'REJECT', '❌ FAIL*'),
    ]
    
    for partition, method, price, expected, result in price_test_cases:
        row_cells = price_results_table.add_row().cells
        row_cells[0].text = partition
        row_cells[1].text = method
        row_cells[2].text = price
        row_cells[3].text = expected
        row_cells[4].text = result
        
        if '✅' in result:
            shade_cell(row_cells[4], 'C6EFCE')  # Green
        elif '❌' in result:
            shade_cell(row_cells[4], 'FFC7CE')  # Red
    
    doc.add_paragraph()
    note1 = doc.add_paragraph()
    note1.add_run('* Note: ').bold = True
    note1.add_run('Failed tests indicate missing validation logic in the system - these are expected failures that reveal areas for improvement.')
    
    # Test 2: MyCartQuantityTest (by Yuqian Chiu)
    doc.add_paragraph()
    add_heading_style(doc, '7.3.2 MyCartQuantityTest (Author: Yuqian Chiu)', 3)
    
    author2_para = doc.add_paragraph()
    author2_para.add_run('Test Author: ').bold = True
    author2_para.add_run('Yuqian Chiu')
    
    file2_para = doc.add_paragraph()
    file2_para.add_run('File Location: ').bold = True
    file2_para.add_run('sm-core/src/test/java/com/salesmanager/test/shoppingcart/MyCartQuantityTest.java')
    
    exec2_para = doc.add_paragraph()
    exec2_para.add_run('Test Execution: ').bold = True
    exec2_para.add_run('4 tests run, 1 passed, 3 failed (expected failures)')
    
    desc2_para = doc.add_paragraph(
        'This test suite validates shopping cart quantity handling across 4 partitions, testing valid quantities, '
        'zero quantity, negative quantities, and over-stock scenarios with a product having 10 items in stock.'
    )
    add_paragraph_spacing(desc2_para)
    
    # ShoppingCart Test Results Table
    cart_results_table = doc.add_table(rows=1, cols=5)
    cart_results_table.style = 'Light Grid Accent 1'
    hdr_cells2 = cart_results_table.rows[0].cells
    hdr_cells2[0].text = 'Partition'
    hdr_cells2[1].text = 'Test Method'
    hdr_cells2[2].text = 'Quantity'
    hdr_cells2[3].text = 'Expected'
    hdr_cells2[4].text = 'Result'
    for cell in hdr_cells2:
        shade_cell(cell, '70AD47')  # Green header
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    # ShoppingCart test cases
    cart_test_cases = [
        ('Partition 1:\nValid Range\n(1-10)', 'testAddToCart_ValidQuantity', '5', 'PASS\n(Within stock)', '✅ PASS'),
        
        ('Partition 2:\nInvalid Negative', 'testAddToCart_NegativeQuantity', '-1', 'REJECT\n(Exception)', '❌ FAIL*'),
        
        ('Partition 3:\nInvalid Zero', 'testAddToCart_ZeroQuantity', '0', 'REJECT\n(Exception)', '❌ FAIL*'),
        
        ('Partition 4:\nOver Stock', 'testAddToCart_OverStock', '11', 'REJECT\n(Exceeds stock)', '❌ FAIL*'),
    ]
    
    for partition, method, qty, expected, result in cart_test_cases:
        row_cells = cart_results_table.add_row().cells
        row_cells[0].text = partition
        row_cells[1].text = method
        row_cells[2].text = qty
        row_cells[3].text = expected
        row_cells[4].text = result
        
        if '✅' in result:
            shade_cell(row_cells[4], 'C6EFCE')  # Green
        elif '❌' in result:
            shade_cell(row_cells[4], 'FFC7CE')  # Red
    
    doc.add_paragraph()
    note2 = doc.add_paragraph()
    note2.add_run('* Note: ').bold = True
    note2.add_run('Failed tests indicate missing validation in ShoppingCartService - the system currently accepts invalid quantities without throwing exceptions.')
    
    # Summary statistics
    doc.add_paragraph()
    doc.add_page_break()
    add_heading_style(doc, '7.4 Test Execution Summary', 2)
    
    summary_intro = doc.add_paragraph(
        'The following tables summarize the execution results for both test suites, highlighting '
        'the test coverage and issues discovered in the Shopizer platform.'
    )
    add_paragraph_spacing(summary_intro)
    
    # Summary for ProductPricePartitionTest
    add_heading_style(doc, '7.4.1 ProductPricePartitionTest Summary (Yijun Sun)', 3)
    
    summary_table1 = doc.add_table(rows=1, cols=2)
    summary_table1.style = 'Light Grid Accent 1'
    hdr_cells = summary_table1.rows[0].cells
    hdr_cells[0].text = 'Metric'
    hdr_cells[1].text = 'Value'
    for cell in hdr_cells:
        shade_cell(cell, '4472C4')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    summary_data1 = [
        ('Test Focus', 'Product Price Validation'),
        ('Total Test Cases', '19'),
        ('Passed Tests', '14 (73.7%)'),
        ('Failed Tests (Expected)', '5 (26.3%)'),
        ('Partitions Covered', '7 (Small/Medium/Large/Very Large/Boundary/Precision/Null)'),
        ('Test Execution Time', '~5 seconds'),
        ('Code Coverage', 'ProductService, ProductPrice, ProductAvailability'),
    ]
    
    for metric, value in summary_data1:
        row_cells = summary_table1.add_row().cells
        row_cells[0].text = metric
        row_cells[1].text = value
    
    doc.add_paragraph()
    
    # Summary for MyCartQuantityTest
    add_heading_style(doc, '7.4.2 MyCartQuantityTest Summary (Yuqian Chiu)', 3)
    
    summary_table2 = doc.add_table(rows=1, cols=2)
    summary_table2.style = 'Light Grid Accent 1'
    hdr_cells2 = summary_table2.rows[0].cells
    hdr_cells2[0].text = 'Metric'
    hdr_cells2[1].text = 'Value'
    for cell in hdr_cells2:
        shade_cell(cell, '70AD47')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    summary_data2 = [
        ('Test Focus', 'Shopping Cart Quantity Validation'),
        ('Total Test Cases', '4'),
        ('Passed Tests', '1 (25%)'),
        ('Failed Tests (Expected)', '3 (75%)'),
        ('Partitions Covered', '4 (Valid/Negative/Zero/OverStock)'),
        ('Test Execution Time', '~5 seconds'),
        ('Code Coverage', 'ShoppingCartService, ShoppingCart, ShoppingCartItem'),
    ]
    
    for metric, value in summary_data2:
        row_cells = summary_table2.add_row().cells
        row_cells[0].text = metric
        row_cells[1].text = value
    
    doc.add_paragraph()
    
    # Combined Summary
    add_heading_style(doc, '7.4.3 Combined Test Summary', 3)
    
    combined_table = doc.add_table(rows=1, cols=2)
    combined_table.style = 'Light Grid Accent 1'
    hdr_cells3 = combined_table.rows[0].cells
    hdr_cells3[0].text = 'Overall Metric'
    hdr_cells3[1].text = 'Value'
    for cell in hdr_cells3:
        shade_cell(cell, '808080')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    combined_data = [
        ('Total Test Cases', '23'),
        ('Total Passed', '15 (65.2%)'),
        ('Total Failed (Expected)', '8 (34.8%)'),
        ('Total Partitions Tested', '11'),
        ('Services Tested', 'ProductService, ShoppingCartService'),
        ('Test Lines of Code', '~400 lines'),
    ]
    
    for metric, value in combined_data:
        row_cells = combined_table.add_row().cells
        row_cells[0].text = metric
        row_cells[1].text = value
    
    # Issues found
    doc.add_paragraph()
    add_heading_style(doc, '7.5 Issues Identified Through Testing', 2)
    
    issues_intro = doc.add_paragraph(
        'During the execution of both test suites, several critical validation gaps were identified '
        'in the Shopizer platform. These findings highlight areas requiring improvement:'
    )
    add_paragraph_spacing(issues_intro)
    
    add_heading_style(doc, '7.5.1 ProductPrice Issues (Discovered by Yijun Sun)', 3)
    
    doc.add_paragraph(
        '❌ Missing Negative Price Validation: The system accepts negative prices (e.g., -$10.00, -$0.01) '
        'without rejection. Recommendation: Add @Min(0) validation annotation and service-layer checks.',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ Null Price Handling: The system does not gracefully handle null prices, potentially leading to '
        'NullPointerException. Recommendation: Add @NotNull validation or implement default value logic.',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ Decimal Precision Validation: Prices with excessive decimal places (e.g., $99.999, $99.123456) '
        'are accepted without proper validation or rounding. Recommendation: Enforce 2-decimal precision at service layer.',
        style='List Bullet'
    )
    doc.add_paragraph(
        '✅ Positive Finding: BigDecimal correctly handles monetary calculations, preventing floating-point errors.',
        style='List Bullet'
    )
    
    doc.add_paragraph()
    add_heading_style(doc, '7.5.2 ShoppingCart Issues (Discovered by Yuqian Chiu)', 3)
    
    doc.add_paragraph(
        '❌ Missing Negative Quantity Validation: The system accepts negative quantities (e.g., -1) '
        'without throwing exceptions. Recommendation: Add quantity validation in ShoppingCartService.create().',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ Zero Quantity Handling: Shopping cart allows items with zero quantity to be added, '
        'which should be rejected. Recommendation: Implement minimum quantity check (quantity >= 1).',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ Missing Stock Validation: The system does not validate quantity against available stock '
        'when adding items to cart. Items exceeding stock (e.g., 11 when stock is 10) are accepted. '
        'Recommendation: Add stock availability check before cart item creation.',
        style='List Bullet'
    )
    doc.add_paragraph(
        '✅ Positive Finding: Valid quantity (1-10) is correctly processed and persisted to the shopping cart.',
        style='List Bullet'
    )
    
    doc.add_paragraph()
    add_heading_style(doc, '7.5.3 Recommendations for Development Team', 3)
    
    recommendations = doc.add_paragraph(
        'Based on the test results from both contributors, we recommend the following improvements:'
    )
    add_paragraph_spacing(recommendations)
    
    doc.add_paragraph(
        '1. Implement comprehensive input validation using Bean Validation (JSR 303) annotations',
        style='List Number'
    )
    doc.add_paragraph(
        '2. Add service-layer validation for business rules (stock availability, price ranges, quantity limits)',
        style='List Number'
    )
    doc.add_paragraph(
        '3. Create custom validators for complex scenarios (e.g., @ValidPrice, @ValidQuantity)',
        style='List Number'
    )
    doc.add_paragraph(
        '4. Improve error handling to provide clear, actionable error messages to API consumers',
        style='List Number'
    )
    doc.add_paragraph(
        '5. Add these partition-based tests to the CI/CD pipeline to prevent regression',
        style='List Number'
    )
    
    # Conclusion
    doc.add_page_break()
    add_heading_style(doc, '8. Conclusion', 1)
    
    conclusion = doc.add_paragraph(
        'This comprehensive testing analysis of the Shopizer e-commerce platform demonstrates '
        'the application of systematic partition-based testing methodology to improve test coverage '
        'and identify critical validation gaps. The collaborative effort between two test engineers '
        'resulted in the following key findings:'
    )
    add_paragraph_spacing(conclusion)
    
    doc.add_paragraph(
        'Shopizer is a mature, well-structured Java enterprise application with ~115K lines of code '
        'organized into 5 Maven modules, employing Spring Boot and modern Java development practices.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'The project employs JUnit 4 and Mockito for testing with existing coverage across key business domains, '
        'providing a solid foundation for additional test development.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Partition-based testing provides a systematic approach to identifying representative test cases, '
        'boundary conditions, and edge cases that might be missed with ad-hoc testing.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Two critical service features were tested: ProductPrice validation (19 test cases across 7 partitions) '
        'and ShoppingCart quantity validation (4 test cases across 4 partitions).',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Testing revealed 8 validation gaps (5 in ProductService, 3 in ShoppingCartService) that represent '
        'potential security and data integrity risks in production.',
        style='List Bullet'
    )
    
    doc.add_paragraph()
    add_heading_style(doc, '8.1 Test Contributions', 2)
    
    contrib_intro = doc.add_paragraph(
        'This testing effort represents a collaborative work between two test engineers, each focusing on '
        'different critical aspects of the Shopizer e-commerce platform:'
    )
    add_paragraph_spacing(contrib_intro)
    
    # Contribution table
    contrib_table = doc.add_table(rows=1, cols=4)
    contrib_table.style = 'Light Grid Accent 1'
    hdr_cells = contrib_table.rows[0].cells
    hdr_cells[0].text = 'Contributor'
    hdr_cells[1].text = 'Test Suite'
    hdr_cells[2].text = 'Focus Area'
    hdr_cells[3].text = 'Test Cases'
    for cell in hdr_cells:
        shade_cell(cell, '203864')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    contrib_data = [
        ('Yijun Sun', 'ProductPricePartitionTest', 'Product Price Validation\n(Catalog Service)', '19 tests\n7 partitions'),
        ('Yuqian Chiu', 'MyCartQuantityTest', 'Shopping Cart Quantity Validation\n(Cart Service)', '4 tests\n4 partitions'),
    ]
    
    for contributor, suite, focus, cases in contrib_data:
        row_cells = contrib_table.add_row().cells
        row_cells[0].text = contributor
        row_cells[1].text = suite
        row_cells[2].text = focus
        row_cells[3].text = cases
    
    doc.add_paragraph()
    
    add_heading_style(doc, '8.2 Value Delivered', 2)
    
    value_para = doc.add_paragraph(
        'The partition-based testing approach demonstrated in this report provides several key benefits:'
    )
    add_paragraph_spacing(value_para)
    
    doc.add_paragraph(
        'Systematic Coverage: Tests cover representative values, boundary conditions, and invalid inputs '
        'for each partition, ensuring comprehensive validation.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Early Defect Detection: 8 validation gaps were discovered before they could impact production, '
        'potentially preventing financial losses and security vulnerabilities.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Maintainable Test Suite: Well-organized, documented test cases that future developers can '
        'understand and extend.',
        style='List Bullet'
    )
    doc.add_paragraph(
        'Knowledge Transfer: Clear documentation of system behavior and business rules through test cases.',
        style='List Bullet'
    )
    
    conclusion_final = doc.add_paragraph(
        '\nBoth test suites implement partition testing best practices and can be integrated into '
        'the continuous integration pipeline. This collaborative approach provides a foundation for expanding test '
        'coverage across additional Shopizer features and ensures robust validation of critical '
        'e-commerce operations. The identified issues should be prioritized for remediation to improve '
        'the platform\'s reliability and security posture.'
    )
    add_paragraph_spacing(conclusion_final)
    
    # Save document
    doc.save('/Users/yijunsun/Documents/Git/shopizerForTest/Shopizer_Test_Report.docx')
    print('✓ Test report generated: Shopizer_Test_Report.docx')

if __name__ == '__main__':
    create_test_report()
