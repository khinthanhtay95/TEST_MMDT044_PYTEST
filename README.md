## Project Overview: Automated Testing with Pytest

In this project, you will develop a comprehensive test suite for Python programs using **pytest**. You will design, implement, and evaluate unit tests for mathematical calculations, data validation pipelines, and object-oriented state management systems.

Writing effective tests requires understanding boundary conditions, exception handling, parameterized testing, reusable fixtures, and evaluating test quality using **mutation testing** and **code coverage**.

The final outcome of this project is a complete automated test suite verified locally and through GitHub Actions autograding.

---

### Learning Objectives

1. **Automated Testing with Pytest:** Design structured unit tests using Pytest and assert statements.
2. **Boundary & Negative Testing:** Identify normal, boundary, and invalid inputs across multiple functional modules.
3. **Parameterized Testing:** Use `@pytest.mark.parametrize` to eliminate duplicate test code.
4. **Exception Testing:** Verify error handling and custom exceptions using `pytest.raises`.
5. **Fixtures and Setup:** Build reusable test fixtures in `conftest.py` with `@pytest.fixture`.
6. **Mutation Testing & Bug Detection:** Evaluate test suite effectiveness against buggy mutant implementations.
7. **Code Coverage:** Measure test coverage using `pytest-cov` to ensure comprehensive code execution.

---

## Submission Guidelines

To submit your project, please ensure you complete all required tasks and follow these instructions carefully.

### 1. Preparation Checklist
Before pushing your final submission, verify that:
* [ ] You have written complete unit tests in `tests/test_calculator.py` for `src/calculator.py`.
* [ ] You have written complete unit tests in `tests/test_data_validator.py` for `src/data_validator.py`.
* [ ] You have written complete unit tests in `tests/test_student_manager.py` for `src/student_manager.py`.
* [ ] You have configured reusable test fixtures in `tests/conftest.py`.
* [ ] Your test suite passes 100% on the reference code when running `pytest tests/`.
* [ ] Your test suite achieves $\ge 85\%$ statement coverage when running `pytest tests/ --cov=src`.
* [ ] You have completed the AI Student Declaration on [PETRA AI](https://www.petraai.org/student) and saved it as `AI_declaration.png` in the repository root.
* [ ] You have completed all sections in `report.md` (with your Name, MMDT ID, GitHub repository URL, video presentation link, and technical discussion). Do not alter the structure of `report.md`.
* [ ] You have recorded a 5–7 minute video presentation (.mp4, face visible) demonstrating test execution and mutation analysis, and uploaded it to YouTube, Google Drive, or Dropbox (with public view access).

### 2. How to Submit
Once everything is ready, commit and push your code to your GitHub repository's `main` or `master` branch:
```bash
git add .
git commit -m "Submit Project 7: Automated Testing with Pytest"
git push origin main
```
The automated autograding system will automatically run tests upon pushing to the `main` or `master` branch.

---

## Checking Grades

You can check your project grades both locally and online via GitHub Actions.

### 1. Locally (Before Submitting)
You can run your tests and check autograder marks on your local machine:
1. Make sure you have installed all dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Run your unit test suite:
   ```bash
   pytest tests/
   ```
3. Run test coverage analysis:
   ```bash
   pytest tests/ --cov=src --cov-report=term-missing
   ```
4. Run the autograder locally:
   ```bash
   pytest autograde_tests/
   ```
   A scorecard summarizing your earned marks will be outputted directly in the terminal under **"AUTOGRADING SCORECARD"**.

### 2. On GitHub (After Submitting)
Every push to the repository triggers the online autograder.
1. Go to the **Actions** tab of your GitHub repository.
2. Select the latest run (e.g., "Autograder Check" or your commit message).
3. Under the run details, view the **Autograding Scorecard** step summary, which details your score out of 70 marks.

---

## Grading Details & Passing Requirements

* **Autograded Score:** **70 marks** (40 marks for test implementation, mutant detection & coverage; 30 marks for `report.md` completion).
* **Manually Graded Score:** **30 marks** (Test code structure, boundary rigor, and video presentation).
* **Total Coursework Marks:** **100 marks**.
* **Deadline:** **October 25, 2026, at 23:59:59**.
* **Late Submission Policy:** A penalty of **-10 marks per day** will be applied for late submissions.
* **Commitment Fee:** Any late, missing, or failed project (score < 70%) will carry a **30,000 MMK commitment fee**, calculated and collected at the end of the 10-week challenge.
