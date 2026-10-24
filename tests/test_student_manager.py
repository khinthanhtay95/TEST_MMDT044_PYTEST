"""Unit tests for src/student_manager.py (Student and StudentManager).

Uses the shared fixtures from tests/conftest.py:
  empty_manager, sample_student, populated_manager, expected_gpas

populated_manager holds 4 students:
  S001 Aung Aung 4.0 | S002 Hla Hla 3.0 | S003 Mya Mya 2.5 | S004 Zaw Zaw 0.5

Test names contain the method name (e.g. "add_student", "remove_student")
so that `pytest -k remove_student` selects exactly those tests.
"""

import pytest

from src.student_manager import Student

# Student: creation and validation

def test_student_init_sets_attributes():
    student = Student("S201", "Thiri", "thiri@mmdt.edu")
    assert student.student_id == "S201"
    assert student.name == "Thiri"
    assert student.email == "thiri@mmdt.edu"
    assert student.grades == {}

def test_student_init_sample_fixture_starts_with_no_grades(sample_student):
    assert sample_student.grades == {}
    assert sample_student.get_gpa() == 0.0

def test_student_init_grades_are_not_shared_between_students():
    first = Student("S101", "Su Su", "su.su@mmdt.edu")
    second = Student("S102", "Nu Nu", "nu.nu@mmdt.edu")
    first.add_grade("AI101", 90)
    assert second.grades == {}, "each Student must get its own grades dict"

@pytest.mark.parametrize("student_id", ["", None, 123], ids=["empty", "none", "int"])
def test_student_init_invalid_id_raises_value_error(student_id):
    with pytest.raises(ValueError, match="student_id must be a non-empty string"):
        Student(student_id, "Aung Aung", "aung.aung@mmdt.edu")

@pytest.mark.parametrize("name", ["", None, 42], ids=["empty", "none", "int"])
def test_student_init_invalid_name_raises_value_error(name):
    with pytest.raises(ValueError, match="name must be a non-empty string"):
        Student("S001", name, "aung.aung@mmdt.edu")

@pytest.mark.parametrize("email", ["", None, "aung.mmdt.edu", 123], ids=["empty", "none", "no_at_sign", "int"])
def test_student_init_invalid_email_raises_value_error(email):
    with pytest.raises(ValueError, match="email must be a valid"):
        Student("S001", "Aung Aung", email)

# Student.add_grade

@pytest.mark.parametrize("score", [0, 0.0, 50, 85.5, 100, 100.0], ids=["0", "0.0", "50", "85.5", "100", "100.0"])
def test_student_add_grade_valid_scores(sample_student, score):
    sample_student.add_grade("AI101", score)
    assert sample_student.grades["AI101"] == pytest.approx(score)

def test_student_add_grade_stores_score_as_float(sample_student):
    sample_student.add_grade("AI101", 90)
    stored = sample_student.grades["AI101"]
    assert stored == 90.0 and isinstance(stored, float)

def test_student_add_grade_same_course_overwrites_old_score(sample_student):
    sample_student.add_grade("AI101", 50)
    sample_student.add_grade("AI101", 95)
    assert sample_student.grades == {"AI101": 95.0}

@pytest.mark.parametrize("score", [-0.01, -1, 100.01, 101], ids=["-0.01", "-1", "100.01", "101"])
def test_student_add_grade_out_of_range_raises_value_error(sample_student, score):
    with pytest.raises(ValueError, match="out of range"):
        sample_student.add_grade("AI101", score)
    assert sample_student.grades == {}, "a rejected grade must not be stored"

@pytest.mark.parametrize("score", ["90", None, True, [90]], ids=["string", "none", "bool", "list"])
def test_student_add_grade_non_numeric_raises_type_error(sample_student, score):
    with pytest.raises(TypeError, match="Score must be numeric"):
        sample_student.add_grade("AI101", score)
    assert sample_student.grades == {}

@pytest.mark.parametrize("course_code", ["", None, 101], ids=["empty", "none", "int"])
def test_student_add_grade_invalid_course_code_raises_value_error(sample_student, course_code):
    with pytest.raises(ValueError, match="course_code must be a non-empty string"):
        sample_student.add_grade(course_code, 90)

# Student.get_gpa

def test_student_get_gpa_with_no_grades_is_zero(sample_student):
    assert sample_student.get_gpa() == 0.0

@pytest.mark.parametrize(
    "score, expected_gpa",
    [
        (100, 4.0), (90, 4.0),        # 90+ -> 4.0 (90 is the boundary)
        (89.99, 3.0), (80, 3.0),      # 80+ -> 3.0
        (79.99, 2.0), (70, 2.0),      # 70+ -> 2.0
        (69.99, 1.0), (60, 1.0),      # 60+ -> 1.0
        (59.99, 0.0), (0, 0.0),       # below 60 -> 0.0
    ],
    ids=lambda v: str(v),
)
def test_student_get_gpa_grade_brackets(sample_student, score, expected_gpa):
    sample_student.add_grade("AI101", score)
    assert sample_student.get_gpa() == expected_gpa, f"score {score} should give GPA {expected_gpa}"

def test_student_get_gpa_averages_all_courses(sample_student):
    for course, score in {"C1": 95, "C2": 85, "C3": 75, "C4": 65, "C5": 55}.items():
        sample_student.add_grade(course, score)
    assert sample_student.get_gpa() == 2.0          # (4 + 3 + 2 + 1 + 0) / 5

def test_student_get_gpa_is_rounded_to_two_decimals(sample_student):
    for course, score in {"C1": 95, "C2": 95, "C3": 85}.items():
        sample_student.add_grade(course, score)
    assert sample_student.get_gpa() == 3.67         # (4 + 4 + 3) / 3 = 3.666...

def test_student_get_gpa_changes_when_grade_is_updated(sample_student):
    sample_student.add_grade("AI101", 95)
    assert sample_student.get_gpa() == 4.0
    sample_student.add_grade("AI101", 65)
    assert sample_student.get_gpa() == 1.0

# StudentManager.add_student

def test_add_student_to_empty_manager_by_instance(empty_manager, sample_student):
    returned = empty_manager.add_student(sample_student)
    assert returned is sample_student
    assert empty_manager.get_total_students() == 1
    assert empty_manager.get_student("S001") is sample_student

def test_add_student_by_parameters_creates_student(empty_manager):
    student = empty_manager.add_student("S010", "Thida", "thida@mmdt.edu")
    assert isinstance(student, Student)
    assert (student.student_id, student.name, student.email) == ("S010", "Thida", "thida@mmdt.edu")
    assert empty_manager.get_student("S010") is student

def test_add_student_several_students_increases_count(empty_manager):
    for i in range(1, 6):
        empty_manager.add_student(f"S{i:03d}", f"Student {i}", f"s{i}@mmdt.edu")
        assert empty_manager.get_total_students() == i

@pytest.mark.parametrize(
    "name, email",
    [(None, "thida@mmdt.edu"), ("Thida", None), (None, None)],
    ids=["no_name", "no_email", "neither"],
)
def test_add_student_by_id_without_name_or_email_raises_value_error(empty_manager, name, email):
    with pytest.raises(ValueError, match="name and email must be provided"):
        empty_manager.add_student("S010", name, email)
    assert empty_manager.get_total_students() == 0

def test_add_student_by_parameters_with_invalid_email_raises_value_error(empty_manager):
    with pytest.raises(ValueError, match="email must be a valid"):
        empty_manager.add_student("S010", "Thida", "not-an-email")
    assert empty_manager.get_total_students() == 0

@pytest.mark.parametrize("bad_argument", [123, None, ["S010"], {"id": "S010"}], ids=["int", "none", "list", "dict"])
def test_add_student_invalid_argument_type_raises_type_error(empty_manager, bad_argument):
    with pytest.raises(TypeError, match="Invalid argument for add_student"):
        empty_manager.add_student(bad_argument)

# duplicate IDs (state must NOT change) 

def test_add_student_duplicate_id_instance_raises_value_error(populated_manager, sample_student):
    # sample_student is S001, and populated_manager already has S001
    with pytest.raises(ValueError, match="already exists"):
        populated_manager.add_student(sample_student)

def test_add_student_duplicate_id_parameters_raises_value_error(populated_manager):
    with pytest.raises(ValueError, match="already exists"):
        populated_manager.add_student("S002", "Someone Else", "else@mmdt.edu")

def test_add_student_duplicate_does_not_overwrite_original(populated_manager, expected_gpas):
    with pytest.raises(ValueError):
        populated_manager.add_student("S001", "Impostor", "impostor@mmdt.edu")
    original = populated_manager.get_student("S001")
    assert original.name == "Aung Aung", "the original record must be kept"
    assert original.get_gpa() == expected_gpas["S001"]
    assert populated_manager.get_total_students() == 4

def test_add_student_same_id_twice_on_empty_manager_raises_value_error(empty_manager):
    empty_manager.add_student("S050", "Ko Ko", "ko.ko@mmdt.edu")
    with pytest.raises(ValueError, match="already exists"):
        empty_manager.add_student("S050", "Ko Ko", "ko.ko@mmdt.edu")
    assert empty_manager.get_total_students() == 1

# StudentManager.get_student / get_all_students / get_total_students

@pytest.mark.parametrize("student_id, name", [("S001", "Aung Aung"), ("S004", "Zaw Zaw")])
def test_get_student_returns_correct_record(populated_manager, student_id, name):
    student = populated_manager.get_student(student_id)
    assert student.student_id == student_id and student.name == name

@pytest.mark.parametrize("student_id", ["S999", "", "s001"], ids=["unknown", "empty", "wrong_case"])
def test_get_student_unknown_id_raises_key_error(populated_manager, student_id):
    with pytest.raises(KeyError, match="not found"):
        populated_manager.get_student(student_id)

def test_get_student_from_empty_manager_raises_key_error(empty_manager):
    with pytest.raises(KeyError):
        empty_manager.get_student("S001")

def test_get_all_students_returns_every_student(populated_manager):
    ids = [s.student_id for s in populated_manager.get_all_students()]
    assert sorted(ids) == ["S001", "S002", "S003", "S004"]

def test_get_all_students_returns_a_copy_of_the_list(populated_manager):
    students = populated_manager.get_all_students()
    students.clear()
    assert populated_manager.get_total_students() == 4

def test_get_total_students_empty_manager_is_zero(empty_manager):
    assert empty_manager.get_total_students() == 0

def test_get_total_students_populated_manager_is_four(populated_manager):
    assert populated_manager.get_total_students() == 4

def test_get_all_students_empty_manager_returns_empty_list(empty_manager):
    assert empty_manager.get_all_students() == []

# StudentManager.update_grade / calculate_gpa

@pytest.mark.parametrize("student_id", ["S001", "S002", "S003", "S004"])
def test_calculate_gpa_matches_expected(populated_manager, expected_gpas, student_id):
    assert populated_manager.calculate_gpa(student_id) == expected_gpas[student_id]

def test_calculate_gpa_unknown_id_raises_key_error(populated_manager):
    with pytest.raises(KeyError, match="not found"):
        populated_manager.calculate_gpa("S999")

def test_update_grade_returns_new_gpa(populated_manager):
    # S004 had 65 (1.0) and 55 (0.0) -> GPA 0.5; raise ML201 to 95 (4.0)
    new_gpa = populated_manager.update_grade("S004", "ML201", 95)
    assert new_gpa == 2.5
    assert populated_manager.calculate_gpa("S004") == 2.5
    assert populated_manager.get_student("S004").grades["ML201"] == 95.0

def test_update_grade_adds_new_course(populated_manager):
    # S002 had 88 and 81 (3.0, 3.0); add a 92 (4.0) -> (3 + 3 + 4) / 3 = 3.33
    new_gpa = populated_manager.update_grade("S002", "DL301", 92)
    assert new_gpa == 3.33
    assert len(populated_manager.get_student("S002").grades) == 3

def test_update_grade_only_changes_that_student(populated_manager, expected_gpas):
    populated_manager.update_grade("S004", "ML201", 95)
    for student_id in ["S001", "S002", "S003"]:
        assert populated_manager.calculate_gpa(student_id) == expected_gpas[student_id]

def test_update_grade_unknown_id_raises_key_error(populated_manager):
    with pytest.raises(KeyError, match="not found"):
        populated_manager.update_grade("S999", "AI101", 90)

@pytest.mark.parametrize(
    "score, error",
    [(101, ValueError), (-5, ValueError), ("A+", TypeError), (None, TypeError)],
    ids=["above_100", "negative", "string", "none"],
)
def test_update_grade_invalid_score_keeps_old_grade(populated_manager, expected_gpas, score, error):
    with pytest.raises(error):
        populated_manager.update_grade("S001", "AI101", score)
    assert populated_manager.get_student("S001").grades["AI101"] == 95.0
    assert populated_manager.calculate_gpa("S001") == expected_gpas["S001"]

# StudentManager.remove_student

def test_remove_student_returns_true(populated_manager):
    assert populated_manager.remove_student("S002") is True

def test_remove_student_decreases_count(populated_manager):
    populated_manager.remove_student("S002")
    assert populated_manager.get_total_students() == 3

def test_remove_student_then_get_student_raises_key_error(populated_manager):
    populated_manager.remove_student("S002")
    with pytest.raises(KeyError, match="not found"):
        populated_manager.get_student("S002")

def test_remove_student_keeps_other_students(populated_manager):
    populated_manager.remove_student("S002")
    remaining = sorted(s.student_id for s in populated_manager.get_all_students())
    assert remaining == ["S001", "S003", "S004"]

def test_remove_student_unknown_id_raises_key_error(populated_manager):
    with pytest.raises(KeyError, match="not found"):
        populated_manager.remove_student("S999")
    assert populated_manager.get_total_students() == 4

def test_remove_student_twice_raises_key_error(populated_manager):
    populated_manager.remove_student("S003")
    with pytest.raises(KeyError, match="not found"):
        populated_manager.remove_student("S003")

def test_remove_student_from_empty_manager_raises_key_error(empty_manager):
    with pytest.raises(KeyError):
        empty_manager.remove_student("S001")

def test_remove_student_then_add_same_id_again(populated_manager):
    populated_manager.remove_student("S001")
    populated_manager.add_student("S001", "New Aung", "new.aung@mmdt.edu")
    assert populated_manager.get_student("S001").name == "New Aung"
    assert populated_manager.calculate_gpa("S001") == 0.0

# StudentManager.get_top_performers

@pytest.mark.parametrize(
    "n, expected_ids",
    [
        (1, ["S001"]),
        (2, ["S001", "S002"]),
        (3, ["S001", "S002", "S003"]),
        (4, ["S001", "S002", "S003", "S004"]),          # n == number of students
        (10, ["S001", "S002", "S003", "S004"]),         # n larger than number of students
    ],
    ids=["n=1", "n=2", "n=3", "n=4_all", "n=10_more_than_students"],
)
def test_get_top_performers_ordered_by_gpa(populated_manager, n, expected_ids):
    top = populated_manager.get_top_performers(n)
    assert [s.student_id for s in top] == expected_ids

def test_get_top_performers_default_is_three(populated_manager):
    assert [s.student_id for s in populated_manager.get_top_performers()] == ["S001", "S002", "S003"]

@pytest.mark.parametrize("n", [0, -1, -10], ids=["n=0", "n=-1", "n=-10"])
def test_get_top_performers_non_positive_n_raises_value_error(populated_manager, n):
    with pytest.raises(ValueError, match="positive integer"):
        populated_manager.get_top_performers(n)

def test_get_top_performers_empty_manager_returns_empty_list(empty_manager):
    assert empty_manager.get_top_performers(3) == []

def test_get_top_performers_includes_both_tied_students(empty_manager):
    for student_id, name, score in [("T1", "Alice", 95), ("T2", "Bob", 92), ("T3", "Cho", 70)]:
        empty_manager.add_student(student_id, name, f"{student_id.lower()}@mmdt.edu")
        empty_manager.update_grade(student_id, "AI101", score)
    top_two = {s.student_id for s in empty_manager.get_top_performers(2)}
    assert top_two == {"T1", "T2"}       # both have GPA 4.0

def test_get_top_performers_reflects_updated_grades(populated_manager):
    populated_manager.update_grade("S004", "AI101", 100)
    populated_manager.update_grade("S004", "ML201", 100)
    top = populated_manager.get_top_performers(2)
    assert {s.student_id for s in top} == {"S001", "S004"}   # both now 4.0

# StudentManager.filter_by_min_gpa

@pytest.mark.parametrize(
    "min_gpa, expected_ids",
    [
        (0.0, ["S001", "S002", "S003", "S004"]),   # lower boundary: everyone
        (0.5, ["S001", "S002", "S003", "S004"]),   # exactly S004's GPA: included
        (0.51, ["S001", "S002", "S003"]),
        (2.5, ["S001", "S002", "S003"]),           # exactly S003's GPA: included
        (3.0, ["S001", "S002"]),                   # exactly S002's GPA: included
        (3.01, ["S001"]),
        (4.0, ["S001"]),                           # upper boundary
    ],
    ids=lambda v: str(v),
)
def test_filter_by_min_gpa_returns_students_at_or_above(populated_manager, min_gpa, expected_ids):
    result = populated_manager.filter_by_min_gpa(min_gpa)
    assert sorted(s.student_id for s in result) == expected_ids

@pytest.mark.parametrize("min_gpa", [-0.01, -1.0, 4.01, 5.0], ids=["-0.01", "-1.0", "4.01", "5.0"])
def test_filter_by_min_gpa_out_of_range_raises_value_error(populated_manager, min_gpa):
    with pytest.raises(ValueError, match="between 0.0 and 4.0"):
        populated_manager.filter_by_min_gpa(min_gpa)

def test_filter_by_min_gpa_empty_manager_returns_empty_list(empty_manager):
    assert empty_manager.filter_by_min_gpa(0.0) == []

# Full state-transition scenario (integration of Student + StudentManager)

def test_student_manager_full_lifecycle(empty_manager):
    manager = empty_manager
    manager.add_student("S100", "Min Min", "min.min@mmdt.edu")          # add
    assert manager.get_total_students() == 1

    assert manager.update_grade("S100", "AI101", 85) == 3.0             # grade
    assert manager.update_grade("S100", "ML201", 95) == 3.5             # second grade
    assert manager.update_grade("S100", "AI101", 95) == 4.0             # update grade

    assert [s.student_id for s in manager.get_top_performers(1)] == ["S100"]
    assert [s.student_id for s in manager.filter_by_min_gpa(4.0)] == ["S100"]

    assert manager.remove_student("S100") is True                       # remove
    assert manager.get_total_students() == 0
    with pytest.raises(KeyError):
        manager.get_student("S100")