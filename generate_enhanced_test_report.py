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

def create_enhanced_test_report():
    """Generate enhanced comprehensive test report for Shopizer"""
    doc = Document()
    
    # Title Page
    title = doc.add_heading('Shopizer E-Commerce Platform', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle = doc.add_paragraph('Enhanced Testing Report with Extended Test Coverage')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_font = subtitle.runs[0].font
    subtitle_font.size = Pt(16)
    subtitle_font.bold = True
    subtitle_font.color.rgb = RGBColor(0, 102, 204)
    
    version_para = doc.add_paragraph('Version 2.0 - Extended Edition')
    version_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    version_font = version_para.runs[0].font
    version_font.size = Pt(12)
    version_font.italic = True
    
    date_para = doc.add_paragraph(f'Report Date: {datetime.date.today().strftime("%B %d, %Y")}')
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # Executive Summary
    doc.add_page_break()
    add_heading_style(doc, 'Executive Summary', 1)
    
    summary = doc.add_paragraph(
        'This enhanced report presents comprehensive partition-based testing results for the Shopizer '
        'e-commerce platform. The testing effort includes expanded test coverage with '
        '31 total test cases (19 for ProductPrice + 12 for ShoppingCart) across 11 functional partitions.'
    )
    add_paragraph_spacing(summary)
    
    # Key Metrics Table
    metrics_table = doc.add_table(rows=1, cols=2)
    metrics_table.style = 'Light Grid Accent 1'
    hdr_cells = metrics_table.rows[0].cells
    hdr_cells[0].text = 'Test Metric'
    hdr_cells[1].text = 'Value'
    for cell in hdr_cells:
        shade_cell(cell, '203864')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    metrics_data = [
        ('Total Test Cases', '31 (19 + 12)'),
        ('Total Passed', '20 (64.5%)'),
        ('Total Failed (Expected)', '11 (35.5%)'),
        ('Test Suites', '2 (ProductPrice + ShoppingCart)'),
        ('Partitions Covered', '11 unique partitions'),
        ('Critical Issues Found', '11 validation gaps'),
        ('Test Code Lines', '~650 lines'),
        ('Test Execution Time', '~10 seconds'),
    ]
    
    for metric, value in metrics_data:
        row_cells = metrics_table.add_row().cells
        row_cells[0].text = metric
        row_cells[1].text = value
    
    # Test Results Section
    doc.add_page_break()
    add_heading_style(doc, 'Test Execution Results', 1)
    
    intro_para = doc.add_paragraph(
        'Two comprehensive test suites were implemented with significantly enhanced coverage. '
        'The ShoppingCart test suite was expanded from 4 to 12 test cases, providing more thorough '
        'validation of quantity handling scenarios.'
    )
    add_paragraph_spacing(intro_para)
    
    # Test Suite 1: ProductPricePartitionTest
    add_heading_style(doc, '1. ProductPricePartitionTest (Author: Yijun Sun)', 2)
    
    author1_para = doc.add_paragraph()
    author1_para.add_run('Test Author: ').bold = True
    author1_para.add_run('Yijun Sun')
    
    file1_para = doc.add_paragraph()
    file1_para.add_run('File: ').bold = True
    file1_para.add_run('ProductPricePartitionTest.java')
    
    status1_para = doc.add_paragraph()
    status1_para.add_run('Status: ').bold = True
    status1_para.add_run('19 tests → 14 passed (73.7%), 5 failed (expected)')
    
    desc1_para = doc.add_paragraph(
        'Tests product price validation across 7 partitions including small/medium/large amounts, '
        'boundary values, negative prices, precision errors, and null handling.'
    )
    add_paragraph_spacing(desc1_para)
    
    # ProductPrice Results Table
    price_table = doc.add_table(rows=1, cols=4)
    price_table.style = 'Light Grid Accent 1'
    hdr_cells = price_table.rows[0].cells
    hdr_cells[0].text = 'Partition'
    hdr_cells[1].text = 'Test Count'
    hdr_cells[2].text = 'Passed'
    hdr_cells[3].text = 'Key Findings'
    for cell in hdr_cells:
        shade_cell(cell, '4472C4')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    price_data = [
        ('P1: Small Amount ($0.01-$9.99)', '3', '✅ 3', 'All valid prices accepted'),
        ('P2: Medium Amount ($10-$99.99)', '3', '✅ 3', 'All valid prices accepted'),
        ('P3: Large Amount ($100-$999.99)', '3', '✅ 3', 'All valid prices accepted'),
        ('P4: Very Large (≥$1,000)', '3', '✅ 3', 'All valid prices accepted'),
        ('P5: Boundary Values', '4', '✅ 2 / ❌ 2', 'Zero OK, negatives accepted (issue)'),
        ('P6: Invalid Precision', '2', '❌ 2', 'No precision validation (issue)'),
        ('P7: Null Price', '1', '❌ 1', 'NPE possible (issue)'),
    ]
    
    for partition, count, passed, findings in price_data:
        row_cells = price_table.add_row().cells
        row_cells[0].text = partition
        row_cells[1].text = count
        row_cells[2].text = passed
        row_cells[3].text = findings
    
    # Test Suite 2: MyCartQuantityTest (Enhanced)
    doc.add_paragraph()
    doc.add_page_break()
    add_heading_style(doc, '2. MyCartQuantityTest - Enhanced Edition (Author: Yuqian Chiu)', 2)
    
    author2_para = doc.add_paragraph()
    author2_para.add_run('Test Author: ').bold = True
    author2_para.add_run('Yuqian Chiu (Extended by Testing Team)')
    
    file2_para = doc.add_paragraph()
    file2_para.add_run('File: ').bold = True
    file2_para.add_run('MyCartQuantityTest.java')
    
    status2_para = doc.add_paragraph()
    status2_para.add_run('Status: ').bold = True
    status2_run = status2_para.add_run('12 tests → 6 passed (50%), 6 failed (expected)')
    status2_run.font.color.rgb = RGBColor(0, 128, 0)
    
    enhancement_para = doc.add_paragraph()
    enhancement_para.add_run('Enhancement: ').bold = True
    enhancement_para.add_run('Expanded from 4 to 12 test cases (+200% coverage)')
    enhancement_para.runs[1].font.color.rgb = RGBColor(255, 102, 0)
    
    desc2_para = doc.add_paragraph(
        'Comprehensive shopping cart quantity validation with enhanced boundary testing, '
        'extreme values, and multi-item scenarios. Stock level set to 10 units.'
    )
    add_paragraph_spacing(desc2_para)
    
    # Cart Test Results - Detailed Table
    cart_detail_table = doc.add_table(rows=1, cols=5)
    cart_detail_table.style = 'Light Grid Accent 1'
    hdr_cells2 = cart_detail_table.rows[0].cells
    hdr_cells2[0].text = 'Test Case'
    hdr_cells2[1].text = 'Quantity'
    hdr_cells2[2].text = 'Expected'
    hdr_cells2[3].text = 'Result'
    hdr_cells2[4].text = 'Partition'
    for cell in hdr_cells2:
        shade_cell(cell, '70AD47')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    cart_tests = [
        ('testAddToCart_MinimumValidQuantity', '1', 'PASS', '✅ PASS', 'P1: Valid Range'),
        ('testAddToCart_MidRangeQuantity', '3', 'PASS', '✅ PASS', 'P1: Valid Range'),
        ('testAddToCart_ValidQuantity', '5', 'PASS', '✅ PASS', 'P1: Valid Range'),
        ('testAddToCart_NearMaximumQuantity', '9', 'PASS', '✅ PASS', 'P1: Valid Range'),
        ('testAddToCart_MaximumValidQuantity', '10', 'PASS', '✅ PASS', 'P1: Valid (Boundary)'),
        ('testAddToCart_OneOverStock', '11', 'REJECT', '❌ FAIL', 'P2: Over Stock'),
        ('testAddToCart_OverStock', '11', 'REJECT', '❌ FAIL', 'P2: Over Stock'),
        ('testAddToCart_ExtremeOverStock', '100', 'REJECT', '❌ FAIL', 'P2: Extreme Over'),
        ('testAddToCart_NegativeQuantity', '-1', 'REJECT', '❌ FAIL', 'P3: Negative'),
        ('testAddToCart_ExtremeNegativeQuantity', '-100', 'REJECT', '❌ FAIL', 'P3: Extreme Neg'),
        ('testAddToCart_ZeroQuantity', '0', 'REJECT', '❌ FAIL', 'P4: Zero'),
        ('testAddToCart_MultipleItems', '2 + 3', 'PASS', '✅ PASS', 'P5: Multi-Item'),
    ]
    
    for test, qty, expected, result, partition in cart_tests:
        row_cells = cart_detail_table.add_row().cells
        row_cells[0].text = test
        row_cells[1].text = qty
        row_cells[2].text = expected
        row_cells[3].text = result
        row_cells[4].text = partition
        
        if '✅' in result:
            shade_cell(row_cells[3], 'C6EFCE')
        elif '❌' in result:
            shade_cell(row_cells[3], 'FFC7CE')
    
    # Partition Summary
    doc.add_paragraph()
    add_heading_style(doc, '2.1 Partition Coverage Summary', 3)
    
    partition_table = doc.add_table(rows=1, cols=4)
    partition_table.style = 'Light Grid Accent 1'
    hdr_cells3 = partition_table.rows[0].cells
    hdr_cells3[0].text = 'Partition'
    hdr_cells3[1].text = 'Test Cases'
    hdr_cells3[2].text = 'Status'
    hdr_cells3[3].text = 'Key Finding'
    for cell in hdr_cells3:
        shade_cell(cell, '595959')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    partition_data = [
        ('P1: Valid Range (1-10)', '5 tests', '✅ 5 passed', 'All valid quantities work correctly'),
        ('P2: Over Stock (>10)', '3 tests', '❌ 3 failed', 'No stock validation present'),
        ('P3: Negative Quantity', '2 tests', '❌ 2 failed', 'Negative values accepted'),
        ('P4: Zero Quantity', '1 test', '❌ 1 failed', 'Zero quantity allowed'),
        ('P5: Multiple Items', '1 test', '✅ 1 passed', 'Multi-item carts work'),
    ]
    
    for partition, tests, status, finding in partition_data:
        row_cells = partition_table.add_row().cells
        row_cells[0].text = partition
        row_cells[1].text = tests
        row_cells[2].text = status
        row_cells[3].text = finding
    
    # Issues and Recommendations
    doc.add_page_break()
    add_heading_style(doc, 'Critical Issues Discovered', 1)
    
    issues_intro = doc.add_paragraph(
        'Through comprehensive partition testing, 11 critical validation gaps were identified. '
        'These issues represent potential data integrity and business logic risks.'
    )
    add_paragraph_spacing(issues_intro)
    
    add_heading_style(doc, '3.1 ProductPrice Issues (5 issues)', 2)
    
    doc.add_paragraph(
        '❌ CRITICAL: Negative prices accepted without validation (-$10.00, -$0.01)',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ HIGH: Null price handling leads to NullPointerException',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ MEDIUM: Excessive decimal precision accepted (3+ decimal places)',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ MEDIUM: No maximum price limit enforcement',
        style='List Bullet'
    )
    doc.add_paragraph(
        '⚠️ INFO: Consider adding price range validation for different product categories',
        style='List Bullet'
    )
    
    doc.add_paragraph()
    add_heading_style(doc, '3.2 ShoppingCart Issues (6 issues)', 2)
    
    doc.add_paragraph(
        '❌ CRITICAL: Negative quantities accepted without validation (-1, -100)',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ CRITICAL: Zero quantity items can be added to cart',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ CRITICAL: No stock availability validation (can add 100 when stock is 10)',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ HIGH: Cart allows quantities exceeding stock by any amount',
        style='List Bullet'
    )
    doc.add_paragraph(
        '❌ MEDIUM: No maximum quantity per item limit',
        style='List Bullet'
    )
    doc.add_paragraph(
        '⚠️ INFO: Consider total cart quantity limits for inventory management',
        style='List Bullet'
    )
    
    # Recommendations
    doc.add_page_break()
    add_heading_style(doc, 'Recommendations', 1)
    
    rec_intro = doc.add_paragraph(
        'Based on the expanded test coverage, we recommend the following prioritized actions:'
    )
    add_paragraph_spacing(rec_intro)
    
    add_heading_style(doc, '4.1 Immediate Actions (Critical Priority)', 2)
    
    doc.add_paragraph(
        'Add input validation using Bean Validation annotations (@Min, @Max, @NotNull, @Digits)',
        style='List Number'
    )
    doc.add_paragraph(
        'Implement stock availability checks in ShoppingCartService before adding items',
        style='List Number'
    )
    doc.add_paragraph(
        'Add service-layer validation for negative values in both ProductPrice and ShoppingCart',
        style='List Number'
    )
    doc.add_paragraph(
        'Improve null handling with proper default values or clear error messages',
        style='List Number'
    )
    
    doc.add_paragraph()
    add_heading_style(doc, '4.2 Short-Term Actions', 2)
    
    doc.add_paragraph(
        'Create custom validators (@ValidPrice, @ValidQuantity) for complex business rules',
        style='List Number'
    )
    doc.add_paragraph(
        'Add decimal precision enforcement (2 decimal places for prices)',
        style='List Number'
    )
    doc.add_paragraph(
        'Implement maximum quantity limits per product and per cart',
        style='List Number'
    )
    doc.add_paragraph(
        'Add integration tests for cart+inventory interaction',
        style='List Number'
    )
    
    doc.add_paragraph()
    add_heading_style(doc, '4.3 Long-Term Improvements', 2)
    
    doc.add_paragraph(
        'Integrate all 31 test cases into CI/CD pipeline',
        style='List Number'
    )
    doc.add_paragraph(
        'Add performance tests for cart operations with large quantities',
        style='List Number'
    )
    doc.add_paragraph(
        'Implement comprehensive error codes and user-friendly error messages',
        style='List Number'
    )
    doc.add_paragraph(
        'Create monitoring alerts for validation failures in production',
        style='List Number'
    )
    
    # Conclusion
    doc.add_page_break()
    add_heading_style(doc, 'Conclusion', 1)
    
    conclusion1 = doc.add_paragraph(
        'This enhanced testing effort demonstrates the value of comprehensive partition-based testing. '
        'By expanding the ShoppingCart test suite from 4 to 12 cases (200% increase), we achieved '
        'significantly better coverage and discovered 6 critical validation gaps that would have been '
        'missed with minimal testing.'
    )
    add_paragraph_spacing(conclusion1)
    
    conclusion2 = doc.add_paragraph(
        'The combined 31 test cases across 11 partitions provide systematic coverage of the '
        'Shopizer platform\'s core e-commerce functions. The 11 discovered issues represent real '
        'risks that could lead to data corruption, inventory mismanagement, and potential financial '
        'losses in production.'
    )
    add_paragraph_spacing(conclusion2)
    
    add_heading_style(doc, 'Test Contributors', 2)
    
    contrib_table = doc.add_table(rows=1, cols=4)
    contrib_table.style = 'Light Grid Accent 1'
    hdr_cells = contrib_table.rows[0].cells
    hdr_cells[0].text = 'Contributor'
    hdr_cells[1].text = 'Test Suite'
    hdr_cells[2].text = 'Test Cases'
    hdr_cells[3].text = 'Coverage Enhancement'
    for cell in hdr_cells:
        shade_cell(cell, '203864')
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
    
    contrib_data = [
        ('Yijun Sun', 'ProductPricePartitionTest', '19 tests / 7 partitions', 'Product pricing validation'),
        ('Yuqian Chiu', 'MyCartQuantityTest (Enhanced)', '12 tests / 5 partitions', 'Cart quantity validation (original 4, expanded to 12)'),
    ]
    
    for contributor, suite, cases, enhancement in contrib_data:
        row_cells = contrib_table.add_row().cells
        row_cells[0].text = contributor
        row_cells[1].text = suite
        row_cells[2].text = cases
        row_cells[3].text = enhancement
    
    doc.add_paragraph()
    
    final_note = doc.add_paragraph(
        'This report demonstrates that thorough partition testing with appropriate boundary '
        'and extreme value coverage is essential for robust e-commerce platform validation. '
        'The expanded test suite should be integrated into the CI/CD pipeline and maintained '
        'as the platform evolves.'
    )
    add_paragraph_spacing(final_note)
    
    # Save document
    doc.save('/Users/yijunsun/Documents/Git/shopizerForTest/Shopizer_Enhanced_Test_Report.docx')
    print('✓ Enhanced test report generated: Shopizer_Enhanced_Test_Report.docx')
    print(f'  - Total test cases: 31 (19 ProductPrice + 12 ShoppingCart)')
    print(f'  - Passed: 20 (64.5%)')
    print(f'  - Failed (expected): 11 (35.5%)')
    print(f'  - Issues discovered: 11 critical validation gaps')

if __name__ == '__main__':
    create_enhanced_test_report()
