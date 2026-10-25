# Project 7 Report: Automated Testing with Pytest

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Pytest Version & Framework:**`, `**GitHub Repository URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information
- **Name:** Khin Than Htay
- **MMDT ID:** MMDT044

---

## Section 1: Test Suite Configuration
- **Pytest Version & Framework:** Pytest-9.1.1 with pytest-cov-7.1.0, Python 3.14.2
- **Total Test Cases Written:** 396 test cases from 116 test functions expanded with @pytest.mark.parametrize. 128 test cases in test_calculator.py (28 functions), 150 test cases in test_data_validator.py (28 functions) and 118 test cases in test_student_manager.py (60 function). All 396 test cases pass on the reference src/ code.
- **Measured Code Coverage (%):** 100% 
- **Key Fixtures Implemented:** sample_student: added one valid student, ID S001, with no grades, empty_manager: a fresh StudentManager with no students, populated_manager: built on empty_manager and added 4 students with different GPA scores, valid_registration_data: a registration dict that passes every validator, expected_gpas: the expected GPA for each populated student to avoid magic numbers for tests

---

## Section 2: Test Case Design & Boundary Analysis
- **Calculator Boundary & Edge Cases:** empty lists and tuples, single items, negative numbers,0 and 1 prime edge cases, float scores, score bounds 0 and 100, out-of-range scores, duplicate maximums, squares of primes, large primes, 0! and negative factorials, zero and negative exponents, zero to a negative power, boolean and non-numeric types
- **Validator Exception Scenarios:** missing fields, weak passwords, invalid domains, missing top-level domain, consecutive dots, whitespace in email and password, password length limits, missing uppercase, lowercase, digit or special character, username length and format, out-of-range, ages, non-string and non-dict inputs, boolean ages
- **Student Manager State Transitions:** student addition, duplicate ID rejection, invalid student details, grade updates, out-of-range grades, GPA bracket boundaries, GPA recalculation, empty GPA, student lookup, student deletion, removing unknown students, top performers ranking, minimum GPA filtering, full add-to-remove lifecycle

---

## Section 3: Local Verification & Feature Checklist
*Check the test modules and features you successfully implemented and verified locally by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Module 1: Calculator Unit Tests with Boundary & Type Assertions (`test_calculator.py`)
- [x] Parameterized Testing with `@pytest.mark.parametrize` for Multiple Input Scenarios
- [x] Module 2: Data Validator Tests with Custom Exception Assertions (`pytest.raises`)
- [x] Module 3: Student Management System Tests with State Mutation & CRUD Verification
- [x] Reusable Pytest Fixtures in `conftest.py` for Modular Test Setup
- [x] Mutation Testing & Bug Detection Verification (Catching Hidden Mutants)
- [x] Code Coverage Analysis with `pytest-cov` (>= 85% Coverage)

---

## Section 4: Deployed and Presentation Information
- **GitHub Repository URL:** https://github.com/khinthanhtay95/TEST_MMDT044_PYTEST
- **Video Presentation Link:** https://drive.google.com/file/d/1aysD2siyJMTQSDAa0xAMl2MF8SHxiCkS/view?usp=share_link

---

## Section 5: Discussion
*Provide your written analysis for each point by replacing the bracket placeholders below:*
- **Explain why a test suite that passes 100% does not guarantee code correctness, and how mutation testing or evaluating tests against buggy code verifies test suite effectiveness.**
    A test suite that passes 100% only shows that the code is worked for checked cases. It cannot guarantee that the code has wether bugs or not. The test suite may check only normal inputs, skip boundary checks or without proper result format. In this project, tests used normal inputs passed on the correct code but caught 0 of the 8 mutants. For example, code coverage has the same limitation also. is_prime(0) runs the line "if n<=1" and the mutant that changes it to "n<1" still passes the test. For such cases, the boundary value of is_prime(1) catches the bug. Mutation testing checks the quality of automatic testing. Small bugs (mutants) are inserted into the code and a strong test suite should fail on all bugs. The mutation score : MS = killed mutants/(total mutants - equivalent mutants). In my test suite with mutation testing, it caught all 8 injected mutants such as duplicate student IDs and registration missing field check.
- **Compare classical unit and integration testing in software engineering with modern AI engineering evaluation (e.g., LLM benchmarks, unit testing AI agents/tool calls, and Process Reward Models / LLM-as-a-judge).**
    Classical unit tests check small part of the code while integration tests check several parts which work together. Both tests are deterministic. For example, the same input always gives the same output. Thus, an exact assert can predict pass or fail output. Modern AI systems are harder to test with them because their outputs can change each run and probabilistic answers. AI engineering evaluation uses scores measured from many examples instead of single exact checks. LLM benchmarks works like huge test suites. For example, HumanEval (developed by OpenAI for python code generation abilities of LLMs) runs unit tests on code written by a model and report pass@k, the probability that at least one of k generated answers passes the test. Unit testing AI agents / tool calls is similar to validate_registrations tests from test_data_validator.py. The arguments much be checked for required fields, correct types and valid ranges before a test tool runs. Process Reward Model scores every reasoning step like unit tests check each part, while checking only the final answer is like a single end-to-end test. LLM-as-a-judge uses another model as the grader. Therefore, it can be biased. Thus, the judge LLM must be tested like mutation testing tests a test suite. 
