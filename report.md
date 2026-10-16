# Project 7 Report: Automated Testing with Pytest

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Pytest Version & Framework:**`, `**GitHub Repository URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information
- **Name:** [Write your Name here]
- **MMDT ID:** [Write your MMDT ID here]

---

## Section 1: Test Suite Configuration
- **Pytest Version & Framework:** [Write your Pytest version and test environment here, e.g., Pytest 7.4.0 with pytest-cov]
- **Total Test Cases Written:** [Write total number of test cases implemented across all test files]
- **Measured Code Coverage (%):** [Write your measured test coverage percentage here, e.g., 95%]
- **Key Fixtures Implemented:** [Describe key fixtures implemented in conftest.py, e.g., sample_student, empty_manager, populated_manager, valid_registration_data]

---

## Section 2: Test Case Design & Boundary Analysis
- **Calculator Boundary & Edge Cases:** [Describe calculator boundary conditions tested, e.g., empty lists, single items, negative numbers, 0 and 1 prime edge cases, float scores]
- **Validator Exception Scenarios:** [Describe data validator exception testing, e.g., missing fields, weak passwords, invalid domains, out-of-range ages]
- **Student Manager State Transitions:** [Describe state mutation and CRUD testing, e.g., student addition, duplicate ID rejection, grade updates, GPA recalculation, student deletion]

---

## Section 3: Local Verification & Feature Checklist
*Check the test modules and features you successfully implemented and verified locally by placing an `x` in the brackets (e.g., `[x]`):*
- [ ] Module 1: Calculator Unit Tests with Boundary & Type Assertions (`test_calculator.py`)
- [ ] Parameterized Testing with `@pytest.mark.parametrize` for Multiple Input Scenarios
- [ ] Module 2: Data Validator Tests with Custom Exception Assertions (`pytest.raises`)
- [ ] Module 3: Student Management System Tests with State Mutation & CRUD Verification
- [ ] Reusable Pytest Fixtures in `conftest.py` for Modular Test Setup
- [ ] Mutation Testing & Bug Detection Verification (Catching Hidden Mutants)
- [ ] Code Coverage Analysis with `pytest-cov` (>= 85% Coverage)

---

## Section 4: Deployed and Presentation Information
- **GitHub Repository URL:** [Provide your public GitHub repository URL here]
- **Video Presentation Link:** [Provide an accessible link to your 5–7 minute video presentation]

---

## Section 5: Discussion
*Provide your written analysis for each point by replacing the bracket placeholders below:*
- **Explain why a test suite that passes 100% does not guarantee code correctness, and how mutation testing or evaluating tests against buggy code verifies test suite effectiveness.**
    [Write your answer here]
- **Compare classical unit and integration testing in software engineering with modern AI engineering evaluation (e.g., LLM benchmarks, unit testing AI agents/tool calls, and Process Reward Models / LLM-as-a-judge).**
    [Write your answer here]
