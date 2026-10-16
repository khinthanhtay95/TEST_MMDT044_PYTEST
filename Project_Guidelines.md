## AI Policy: Use & Declaration
- **Limited AI Use:** AI coding assistants (e.g., GitHub Copilot) may be used for syntax suggestions, debugging, coding support, and learning assistance.
- **Prohibited:** Do not paste project prompts, guidelines, problem statements, or substantial portions of project materials into AI systems for code generation, completion, or debugging.
- **Responsibility:** Submitted work must reflect your own understanding, implementation, and problem-solving effort.

### AI Use Declaration

1. Complete the [PETRA AI Student Declaration](https://www.petraai.org/student) based on your actual AI use for this project.
2. Generate and save the declaration image as **`AI_declaration.png`**.
3. Include **`AI_declaration.png`** in your project repository root.

> **Required:** Your declaration must accurately reflect how you used AI tools for this project.

---

## Project Overview: Automated Testing with Pytest

In this project, you will build and evaluate a comprehensive automated testing repository called **MMDT_tests** using Python and `pytest`.

Writing reliable, robust code requires more than just checking that code runs on happy paths. As software systems and AI applications grow in complexity, developers must anticipate edge cases, boundary inputs, type mismatches, and exceptional conditions. The primary goal of this project is to develop your testing mindset: learning how to systematically identify test scenarios, write parameterized unit tests, build reusable test fixtures, assert error states, and measure the bug-detecting power of your test suite through mutation testing.

The final outcome of this project is a fully verified Pytest test suite, high coverage reports, and a submitted analysis report.

---

### Learning Objectives

1. **Automated Testing Principles:** Understand the role of automated unit and integration tests in ensuring software correctness, regression prevention, and reliability.
2. **Boundary & Edge Case Analysis:** Identify normal, boundary, and invalid input spaces to design comprehensive test matrices.
3. **Pytest Implementation & Assertions:** Master standard Pytest syntax, assertion introspection, and test structuring.
4. **Parameterized Testing:** Utilize `@pytest.mark.parametrize` to run tests over multiple input/expected pairs efficiently without code duplication.
5. **Exception & Error Handling Testing:** Verify defensive programming mechanisms and custom exceptions using `pytest.raises`.
6. **Reusable Test Fixtures:** Implement test data setup and teardown using `@pytest.fixture` in `conftest.py`.
7. **Test Suite Quality & Mutation Testing:** Understand why 100% pass rates do not guarantee correctness, and evaluate test suite efficacy against intentionally flawed / buggy implementations (mutants).
8. **Test Coverage Analysis:** Measure and interpret statement and branch coverage using `pytest-cov`.
9. **Connections to Modern AI Engineering:** Relate traditional unit testing principles to modern AI evaluation benchmarks, tool-use validation in AI agents, and Process Reward Models.

---

## Your Job

1. Study the source modules provided under `src/`:
   - `src/calculator.py`: Basic mathematical and statistical functions (`calculate_average`, `find_maximum`, `is_prime`, `factorial`, `power`).
   - `src/data_validator.py`: Registration and field validation with custom exceptions (`validate_email`, `validate_password`, `validate_username`, `validate_age`, `validate_registration`).
   - `src/student_manager.py`: Object state management and student grade tracking (`Student`, `StudentManager`).
2. Write comprehensive unit test suites under `tests/`:
   - `tests/test_calculator.py`: Test all calculator functions across normal, boundary, and invalid inputs.
   - `tests/test_data_validator.py`: Test data validation rules, invalid formats, and custom exception raising.
   - `tests/test_student_manager.py`: Test student creation, grade updating, GPA calculation, removal, and queries.
   - `tests/conftest.py`: Define reusable test fixtures for test data setup.
3. Verify that your test suite passes 100% on the reference `src/` implementations (`pytest tests/`).
4. Evaluate test suite bug detection effectiveness against buggy mutants (`pytest autograde_tests/`).
5. Ensure your test suite achieves high code coverage on `src/` (`pytest tests/ --cov=src`).
6. Complete all required sections in `report.md`.
7. Complete the PETRA AI Student Declaration and save it as `AI_declaration.png` in the repository root.
8. Record a 5–7 minute video presentation explaining your test design, boundary conditions, fixtures, and mutation testing takeaways.

---

### 📋 Task 1: Module 1 — Basic Calculator Test Suite (`tests/test_calculator.py`)

Write tests for functions in `src/calculator.py`:
- `calculate_average(scores)`:
  - Valid score lists (normal cases, boundary scores 0 and 100, float scores, single-item lists).
  - Empty list raising `ValueError`.
  - Out-of-bounds scores (< 0 or > 100) raising `ValueError`.
  - Invalid types (non-list, non-numeric elements, booleans) raising `TypeError`.
- `find_maximum(numbers)`:
  - Positive numbers, negative numbers, mixed numbers, single-element lists, lists with duplicate maximums.
  - Empty list raising `ValueError`.
  - Invalid types raising `TypeError`.
- `is_prime(n)`:
  - Numbers $\le 1$ returning `False` (negative numbers, 0, 1).
  - Small primes (2, 3) returning `True`.
  - Even numbers > 2 returning `False`.
  - Composite odd numbers (9, 15, 25, 49) returning `False`.
  - Large prime numbers (29, 97) returning `True`.
  - Non-integer types (floats, booleans, strings) raising `TypeError`.
- `factorial(n)` & `power(base, exponent)`:
  - Valid calculations (0! = 1, positive factorials, powers with positive/zero/negative exponents).
  - Negative factorial input raising `ValueError`.
  - 0 raised to a negative exponent raising `ValueError` (division by zero).
  - Invalid input types raising `TypeError`.

> [!TIP]
> Use `@pytest.mark.parametrize` to test multiple input-output combinations cleanly.

---

### 📋 Task 2: Module 2 — Data Validation & Exception Testing (`tests/test_data_validator.py`)

Write tests for data validation in `src/data_validator.py`:
- `validate_email(email)`:
  - Valid email addresses (standard, subdomains, plus addressing).
  - Invalid email formats (empty string, missing `@`, missing domain, missing top-level domain, consecutive dots, whitespace) raising `InvalidEmailError`.
  - Non-string inputs raising `TypeError`.
- `validate_password(password)`:
  - Strong passwords meeting length (8–128), uppercase, lowercase, digit, and special character rules.
  - Weak passwords violating specific rules raising `WeakPasswordError` (with proper error message assertion).
  - Non-string inputs raising `TypeError`.
- `validate_username(username)`:
  - Valid usernames (3–20 chars, starting with letter, alphanumeric/underscore).
  - Invalid usernames (length < 3 or > 20, starting with digit/underscore, special characters, spaces) raising `InvalidUsernameError`.
- `validate_age(age)`:
  - Valid ages in range [13, 120].
  - Out-of-bounds ages (< 13 or > 120) raising `InvalidAgeError`.
  - Non-integer / boolean types raising `TypeError`.
- `validate_registration(data)`:
  - Valid dictionary payload returning `True`.
  - Missing required fields raising `ValidationError`.
  - Invalid child field values propagating proper validation errors.
  - Non-dictionary payload raising `TypeError`.

> [!TIP]
> Use `with pytest.raises(ExpectedException, match="regex_pattern"):` to verify both exception type and message content.

---

### 📋 Task 3: Module 3 — Student Management System & Fixtures (`tests/test_student_manager.py` & `tests/conftest.py`)

Write tests for `Student` and `StudentManager` in `src/student_manager.py`:
- Define shared fixtures in `tests/conftest.py`:
  - `empty_manager`: A fresh `StudentManager` instance.
  - `sample_student`: A single valid `Student` instance.
  - `populated_manager`: A `StudentManager` loaded with multiple students and grades.
  - `valid_registration_data`: A valid registration dictionary fixture.
- Test `Student` class:
  - Attribute initialization and validation on ID, name, email.
  - Adding course grades within bounds [0, 100].
  - Rejecting out-of-bounds grades (`ValueError`) and non-numeric types (`TypeError`).
  - GPA calculation across different letter/score brackets (90+, 80+, 70+, 60+, <60) on a 4.0 scale.
  - Empty grade list returning `0.0`.
- Test `StudentManager` class:
  - Adding students (by `Student` instance and by parameters).
  - Rejecting duplicate `student_id` with `ValueError`.
  - Retrieving students by ID (`get_student`) and raising `KeyError` for unknown IDs.
  - Updating grades (`update_grade`) and checking updated GPA.
  - Removing students (`remove_student`), verifying count decreases and subsequent retrieval raises `KeyError`.
  - Ranking students (`get_top_performers(n)`) and handling boundary `n`.
  - Filtering students by minimum GPA (`filter_by_min_gpa`).

---

### 📋 Task 4: Test Suite Quality & Mutation Bug Detection

A test suite that passes 100% on correct code is only half the battle. A truly robust test suite must **fail** when run against buggy code.

In this project, the autograder executes your test suite against a collection of **mutant implementations** containing subtle, intentional bugs (e.g., boundary off-by-one errors, missing exception raises, bypassed validation rules, duplicate ID overwrite bugs).

To maximize your score on Task 1.3:
- Ensure your test suite contains boundary assertions (e.g. testing `1` and `0` for `is_prime`).
- Verify that your tests assert exception raising when invalid inputs are passed.
- Ensure your tests check that duplicate IDs cannot overwrite existing records.

---

### 📋 Task 5: Complete the Report (`report.md`)

Complete all required sections in [report.md](report.md):
- **Student Information:** Full Name and MMDT ID.
- **Test Suite Configuration:** Document your Pytest environment, total tests written, measured code coverage, and key fixtures.
- **Test Case Design & Boundary Analysis:** Document boundary scenarios, validator edge cases, and state transitions.
- **Local Verification Checklist:** Mark verified test modules and features with `[x]`.
- **Deployed and Presentation Information:** GitHub repository URL and video presentation link.
- **Discussion:** Detailed answers explaining Mutation Testing / Test Effectiveness and comparing classical testing with modern AI system evaluation.

> [!WARNING]
> Do not modify the section headers, bold titles, or overall formatting of [report.md](report.md). Changes to the structure may cause the autograder tests to fail.
> Replace all bracketed placeholder text with your answers. Do not leave any placeholders in the final report.

---

### 📋 Task 6: Record a Video Presentation

Record a **5–7 minute video presentation** explaining your testing implementation:
- **Test Strategy & Matrix:** Explain how you designed test cases covering normal, boundary, and negative scenarios.
- **Pytest Advanced Features:** Demonstrate how you used `@pytest.mark.parametrize`, `pytest.raises`, and `@pytest.fixture`.
- **Bug Detection & Mutation Testing:** Explain why passing tests on correct code does not guarantee quality, and discuss how your tests caught bugs.
- **AI Connections:** Discuss the role of automated verification in modern AI pipelines (e.g., benchmarking LLMs, unit testing AI tool calling).

#### Video Requirements
- You may use tools such as Zoom, Loom, or OBS Studio to record your presentation.
- Your face must be visible during the presentation. If you are not comfortable with this requirement, please discuss it with the instructor in advance.
- The recorded video must be in `.mp4` format and must not exceed **7 minutes**.
- Upload the video to a sharing platform such as YouTube, Google Drive, or Dropbox.
- Ensure the video link is publicly accessible to the instructor.
- Add the video link to Section 4 of `report.md`.

---

## Marking Scheme (70 marks Autograde + 30 marks Manual Grade = 100 marks Total)

### 1. Implementation & Test Suite (40 marks) - Autograded
- **Required Files Check (10 marks):** All required source, test, configuration, and report files present (`src/calculator.py`, `src/data_validator.py`, `src/student_manager.py`, `tests/conftest.py`, `tests/test_calculator.py`, `tests/test_data_validator.py`, `tests/test_student_manager.py`, `requirements.txt`, `report.md`, `AI_declaration.png`).
- **Reference Implementation Pass Check (10 marks):** Student test suite passes 100% against the reference correct implementations without errors.
- **Mutation Bug Detection Effectiveness (15 marks):** Student test suite successfully detects and fails on subtle buggy mutants.
- **Code Coverage Benchmark (5 marks):** Student test suite achieves $\ge 85\%$ statement coverage on `src/`.

### 2. Completion of report.md (30 marks) - Autograded
- **Student Information (5 marks):** Full Name and MMDT ID filled in.
- **Test Suite Configuration (5 marks):** Pytest version, test count, coverage %, and fixtures documented.
- **Complexity & Boundary Analysis (5 marks):** Boundary conditions, exception scenarios, and state transitions documented.
- **Local Verification Checklist (5 marks):** Checklist showing verified test areas marked with `[x]`.
- **Repository & Presentation Details (5 marks):** Provide valid GitHub repository URL and video presentation link.
- **Discussion & Technical Analysis (5 marks):** Comprehensive answers explaining mutation testing and comparing software testing with AI evaluation systems.

### 3. Test Code Quality, Correctness & Video Presentation (30 marks)
**Note:** This section is manually graded.
- **Test Architecture & Pytest Best Practices (10 marks):** Clean test structure, effective fixture reuse, meaningful test names, and proper parametrization.
- **Boundary & Exception Rigor (10 marks):** Depth of edge case exploration, negative testing, and descriptive assertion error messages.
- **Video Presentation (10 marks):** The 5–7 minute presentation clearly demonstrates test execution, coverage reports, and effectively explains testing principles and AI connections.
