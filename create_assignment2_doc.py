#!/usr/bin/env python3
"""
Generate Assignment 2 Test Report in DOCX format
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_assignment2_report():
    # Create document
    doc = Document()
    
    # Set normal style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    
    # Title page
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('Shopizer E-Commerce Platform')
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 51, 102)
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Assignment 2: Functional Testing with Finite State Machines\\n')
    run.font.size = Pt(14)
    run = subtitle.add_run('Product Lifecycle FSM Test Suite')
    run.font.size = Pt(14)
    
    doc.add_paragraph()
    
    # Metadata
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('Course: Software Testing\\n')
    info.add_run('Student: Yijun Sun\\n')
    info.add_run('Date: February 7, 2026\\n')
    info.add_run('Module: Product Price & Lifecycle Management')
    
    doc.add_page_break()
    
    # Table of Contents
    doc.add_heading('Table of Contents', level=1)
    
    toc_items = [
        '1. Introduction',
        '2. Why Finite State Machines are Useful for Testing',
        '3. Feature Selection: Product Lifecycle Management',
        '4. FSM Model Design',
        '5. Test Coverage and Implementation',
        '6. Test Execution Results',
        '7. Defects and Issues Found',
        '8. Conclusions',
        '9. Team Contribution: Shopping Cart FSM (Yuqian Chiu)',
    ]
    
    for item in toc_items:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_page_break()
    
    # Section 1: Introduction
    doc.add_heading('1. Introduction', level=1)
    
    intro = """This report documents the implementation of a comprehensive test suite for Product Lifecycle Management using Finite State Machine (FSM) modeling. Building upon Assignment 1's price partition testing (19 test cases covering 7 price partitions), this assignment extends testing to the complete product lifecycle from creation to archival."""
    
    doc.add_paragraph(intro)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 1: ').bold = True
    run = p.add_run('[INSERT: Overview diagram showing Assignment 1 + Assignment 2 integration]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_page_break()
    
    # Section 2: Why FSM
    doc.add_heading('2. Why Finite State Machines are Useful for Testing', level=1)
    
    fsm_text = """A Finite State Machine (FSM) is a mathematical model with:
• Q: Finite set of states
• Σ: Set of input events
• δ: Transition function
• q₀: Initial state
• F: Final states

FSM Testing Benefits:
• Complete Coverage: All states and transitions tested
• Invalid Transition Detection: Catches illegal state changes
• Guard Condition Validation: Tests preconditions
• Path Testing: Systematic state sequence testing"""
    
    doc.add_paragraph(fsm_text)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 2: ').bold = True
    run = p.add_run('[INSERT: Diagram comparing "Without FSM" vs "With FSM" benefits]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_page_break()
    
    # Section 3: Feature Selection
    doc.add_heading('3. Feature Selection: Product Lifecycle Management', level=1)
    
    doc.add_paragraph('The product lifecycle is "non-trivial" because:')
    
    criteria = [
        'Multiple States: 6 states (DRAFT, PENDING, ACTIVE, MODIFIED, INACTIVE, ARCHIVED)',
        'Complex Transitions: 8 main transitions',
        'Guard Conditions: Price validation, category requirements',
        'Real-World Complexity: Models actual e-commerce workflows',
    ]
    
    for criterion in criteria:
        doc.add_paragraph(criterion, style='List Bullet')
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 3: ').bold = True
    run = p.add_run('[INSERT: Flowchart showing Assignment 1 price partitions → Assignment 2 FSM guards]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_page_break()
    
    # Section 4: FSM Model Design
    doc.add_heading('4. FSM Model Design', level=1)
    
    doc.add_heading('4.1 State Definitions', level=2)
    
    # State table
    table = doc.add_table(rows=7, cols=3)
    table.style = 'Light Grid Accent 1'
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'State'
    hdr_cells[1].text = 'Available'
    hdr_cells[2].text = 'Description'
    
    states = [
        ('DRAFT', 'false', 'Initial creation, editing'),
        ('PENDING', 'false', 'Awaiting approval'),
        ('ACTIVE', 'true', 'Live in catalog'),
        ('MODIFIED', 'true', 'Updated, pending validation'),
        ('INACTIVE', 'false', 'Temporarily removed'),
        ('ARCHIVED', 'false', 'Permanently removed'),
    ]
    
    for i, (state, avail, desc) in enumerate(states, 1):
        row = table.rows[i].cells
        row[0].text = state
        row[1].text = avail
        row[2].text = desc
    
    doc.add_paragraph()
    
    doc.add_heading('4.2 State Diagram', level=2)
    
    doc.add_paragraph('Complete product lifecycle FSM with all states and transitions:')
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 4: ').bold = True
    run = p.add_run('[INSERT: State diagram with 6 states and 8 transitions T1-T8, use colors for states]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_page_break()
    
    # Section 5: Test Implementation
    doc.add_heading('5. Test Coverage and Implementation', level=1)
    
    doc.add_heading('5.1 Test Suite Structure', level=2)
    
    structure = """ProductLifecycleStateMachineTest.java contains 20 test cases:
• State Tests: 6 tests verify each state
• Transition Tests: 8 tests for valid transitions
• Guard Tests: 3 tests validate guards
• Invalid Transition Tests: 2 tests
• Complete Lifecycle Test: 1 full path test"""
    
    doc.add_paragraph(structure)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 5: ').bold = True
    run = p.add_run('[INSERT: IDE showing ProductLifecycleStateMachineTest.java with all 20 test methods]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_paragraph()
    
    doc.add_heading('5.2 Sample Test Cases', level=2)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 6: ').bold = True
    run = p.add_run('[INSERT: Code snippet of testTransition1_DraftToPendingValid() method]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 7: ').bold = True
    run = p.add_run('[INSERT: Code snippet of testTransition4_ActiveToModifiedInvalidPrice() showing guard violation]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_page_break()
    
    # Section 6: Test Results
    doc.add_heading('6. Test Execution Results', level=1)
    
    doc.add_heading('6.1 Test Environment', level=2)
    
    env_items = [
        'Framework: JUnit 4',
        'Database: H2 in-memory',
        'Transaction: Isolated per test',
        'Date: February 7, 2026',
    ]
    
    for item in env_items:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_paragraph()
    
    doc.add_heading('6.2 Execution Summary', level=2)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 8: ').bold = True
    run = p.add_run('[INSERT: JUnit test results showing all 20 tests executed]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_paragraph()
    
    summary = """Test Results:
• Total: 20 tests
• Passed (Correct): 15 tests
• Passed (Bug Found): 5 tests
• Failed: 0 tests
• Bugs Discovered: 5 validation issues"""
    
    doc.add_paragraph(summary)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 9: ').bold = True
    run = p.add_run('[INSERT: Console output showing test transitions with checkmarks]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_page_break()
    
    # Section 7: Defects
    doc.add_heading('7. Defects and Issues Found', level=1)
    
    doc.add_paragraph('Total defects: 5 critical validation issues')
    
    # Bug table
    table = doc.add_table(rows=6, cols=3)
    table.style = 'Light Grid Accent 1'
    
    hdr = table.rows[0].cells
    hdr[0].text = 'Bug ID'
    hdr[1].text = 'Severity'
    hdr[2].text = 'Description'
    
    bugs = [
        ('BUG-FSM-01', 'High', 'Negative prices accepted'),
        ('BUG-FSM-02', 'High', 'Null prices not rejected'),
        ('BUG-FSM-03', 'Medium', 'No exception for invalid prices'),
        ('BUG-FSM-04', 'Medium', 'Products without categories'),
        ('BUG-FSM-05', 'Low', 'Zero inventory allowed'),
    ]
    
    for i, (bug_id, severity, desc) in enumerate(bugs, 1):
        row = table.rows[i].cells
        row[0].text = bug_id
        row[1].text = severity
        row[2].text = desc
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 10: ').bold = True
    run = p.add_run('[INSERT: Console showing warning "⚠ Warning: System allowed negative price"]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_page_break()
    
    # Section 8: Conclusions
    doc.add_heading('8. Conclusions', level=1)
    
    doc.add_heading('8.1 Summary', level=2)
    
    summary_text = """Assignment 2 Deliverables:
✅ FSM Theory (10%): Explained FSM benefits
✅ Feature Selection (20%): Product Lifecycle (6 states, 8 transitions)
✅ FSM Design (35%): State diagram, transition table, guards
✅ JUnit Implementation (35%): 20 test cases

Total: 39 test cases (19 from Assignment 1 + 20 from Assignment 2)"""
    
    doc.add_paragraph(summary_text)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 11: ').bold = True
    run = p.add_run('[INSERT: Integration diagram showing Assignment 1 → Assignment 2]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_paragraph()
    
    doc.add_heading('8.2 Key Achievements', level=2)
    
    achievements = [
        'Comprehensive 6-state FSM model',
        'Integrated Assignment 1 price validation as guards',
        'Discovered 5 critical bugs',
        'Complete test coverage',
    ]
    
    for achievement in achievements:
        doc.add_paragraph(achievement, style='List Bullet')
    
    doc.add_page_break()
    
    # Section 9: Team Contribution (Yuqian Chiu)
    doc.add_heading('9. Team Contribution: Shopping Cart FSM (Yuqian Chiu)', level=1)

    doc.add_heading('9.1 Overview', level=2)
    doc.add_paragraph(
        'This section documents the FSM testing work completed by team member Yuqian Chiu. '
        'Building on the same FSM principles described in Section 2, Yuqian applied the FSM '
        'methodology to test the Shopping Cart component, ensuring complete independence from '
        'the Product Lifecycle testing covered in previous sections.'
    )

    doc.add_heading('9.2 Feature Selection (Task 2)', level=2)
    doc.add_paragraph(
        'Feature selected: Shopping Cart component. The cart transitions through distinct states '
        '(EMPTY, ACTIVE, OBSOLETE) based on user actions. The model is non-trivial because the '
        'validity of user actions depends on the current state (e.g., updating quantity in EMPTY is invalid, '
        'removing the last item from ACTIVE returns to EMPTY, deleting a cart moves it to OBSOLETE).'
    )

    doc.add_heading('9.3 Functional Model (Task 3)', level=2)
    doc.add_paragraph('State Diagram and Transitions:')
    doc.add_paragraph('• Add Item: EMPTY → ACTIVE')
    doc.add_paragraph('• Update Quantity: ACTIVE → ACTIVE (self-loop)')
    doc.add_paragraph('• Remove Item (last item): ACTIVE → EMPTY')
    doc.add_paragraph('• Delete Cart: ANY → OBSOLETE')

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 13: ').bold = True
    run = p.add_run('[INSERT: Shopping Cart FSM state diagram with EMPTY/ACTIVE/OBSOLETE]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)

    doc.add_heading('9.4 Test Implementation (Task 4)', level=2)
    doc.add_paragraph(
        'Test implementation in MyCartStateTest.java. Strategy ensures 100% transition coverage '
        'via two scenarios: (1) Standard lifecycle (EMPTY → ACTIVE → ACTIVE → EMPTY → OBSOLETE) '
        'and (2) Force deletion (ACTIVE → OBSOLETE).'
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 14: ').bold = True
    run = p.add_run('[INSERT: MyCartStateTest.java code for both scenarios]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 15: ').bold = True
    run = p.add_run('[INSERT: JUnit execution result for MyCartStateTest.java]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)

    doc.add_page_break()

    # Appendix
    doc.add_heading('Appendix: Test Execution Log', level=1)
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('📷 SCREENSHOT 12: ').bold = True
    run = p.add_run('[INSERT: Complete console output showing all 20 test executions]')
    run.italic = True
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    doc.add_paragraph()
    
    log_sample = """Sample Log:
=== Test 1: DRAFT State Creation ===
✓ State DRAFT verified

=== Test 4: DRAFT → PENDING ===
✓ Transition successful

=== Test 10: Invalid Price ===
⚠ Warning: Negative price accepted (bug)

=== Test 20: Complete Lifecycle ===
✓ All 6 states tested"""
    
    doc.add_paragraph(log_sample)
    
    doc.add_paragraph()
    end_para = doc.add_paragraph('--- End of Report ---')
    end_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Save
    output_path = 'test-reports/Assignment2_Test_Report.docx'
    doc.save(output_path)
    
    print(f'✅ Document created: {output_path}')
    print('\\n📸 Screenshot Insertion Guide:')
    print('=' * 60)
    print('Total screenshots needed: 15\\n')
    
    screenshots = [
        ('1', 'Section 1', 'Overview: Assignment 1 + Assignment 2 integration diagram'),
        ('2', 'Section 2', 'FSM benefits comparison diagram'),
        ('3', 'Section 3', 'Assignment 1 partitions → Assignment 2 guards flowchart'),
        ('4', 'Section 4.2', 'State diagram with 6 states and 8 transitions (use colors)'),
        ('5', 'Section 5.1', 'IDE screenshot showing all 20 test methods'),
        ('6', 'Section 5.2', 'Code: testTransition1_DraftToPendingValid()'),
        ('7', 'Section 5.2', 'Code: testTransition4_ActiveToModifiedInvalidPrice()'),
        ('8', 'Section 6.2', 'JUnit execution results (all 20 tests)'),
        ('9', 'Section 6.2', 'Console output with transition success messages'),
        ('10', 'Section 7', 'Console warnings for bugs found'),
        ('11', 'Section 8', 'Integration diagram (Assignment 1 → 2)'),
        ('12', 'Appendix', 'Complete test execution log'),
        ('13', 'Section 9.3', 'Shopping Cart FSM state diagram (EMPTY/ACTIVE/OBSOLETE)'),
        ('14', 'Section 9.4', 'MyCartStateTest.java code for both scenarios'),
        ('15', 'Section 9.4', 'JUnit execution result for MyCartStateTest.java'),
    ]
    
    for num, section, description in screenshots:
        print(f'{num:2}. [{section:12}] {description}')
    
    print('\\n' + '=' * 60)
    print('✅ Document ready for screenshots!')

if __name__ == '__main__':
    create_assignment2_report()
