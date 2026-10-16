"""Student Manager mutants with intentional bugs."""
from typing import Dict, List, Optional
from src.student_manager import Student


# Mutant 1: StudentManager does not raise ValueError on duplicate student ID (silently overwrites)
class StudentManagerMutant1:
    def __init__(self):
        self._students: Dict[str, Student] = {}

    def add_student(self, student_or_id, name: Optional[str] = None, email: Optional[str] = None) -> Student:
        if isinstance(student_or_id, Student):
            student = student_or_id
        elif isinstance(student_or_id, str):
            if name is None or email is None:
                raise ValueError("name and email must be provided.")
            student = Student(student_id=student_or_id, name=name, email=email)
        else:
            raise TypeError("Invalid argument.")
        # BUG: Does NOT check if student.student_id is in self._students!
        self._students[student.student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        if student_id not in self._students:
            raise KeyError(f"Student '{student_id}' not found.")
        return self._students[student_id]

    def update_grade(self, student_id: str, course_code: str, score: float) -> float:
        student = self.get_student(student_id)
        student.add_grade(course_code, score)
        return student.get_gpa()

    def calculate_gpa(self, student_id: str) -> float:
        student = self.get_student(student_id)
        return student.get_gpa()

    def remove_student(self, student_id: str) -> bool:
        if student_id not in self._students:
            raise KeyError(f"Student '{student_id}' not found.")
        del self._students[student_id]
        return True

    def get_all_students(self) -> List[Student]:
        return list(self._students.values())

    def get_total_students(self) -> int:
        return len(self._students)

    def get_top_performers(self, n: int = 3) -> List[Student]:
        if n <= 0:
            raise ValueError("n must be positive.")
        return sorted(self._students.values(), key=lambda s: (s.get_gpa(), s.name), reverse=True)[:n]

    def filter_by_min_gpa(self, min_gpa: float) -> List[Student]:
        if min_gpa < 0.0 or min_gpa > 4.0:
            raise ValueError("min_gpa out of range.")
        return [s for s in self._students.values() if s.get_gpa() >= min_gpa]


# Mutant 2: StudentManager remove_student does not raise KeyError when removing non-existent student
class StudentManagerMutant2:
    def __init__(self):
        self._students: Dict[str, Student] = {}

    def add_student(self, student_or_id, name: Optional[str] = None, email: Optional[str] = None) -> Student:
        if isinstance(student_or_id, Student):
            student = student_or_id
        elif isinstance(student_or_id, str):
            if name is None or email is None:
                raise ValueError("name and email must be provided.")
            student = Student(student_id=student_or_id, name=name, email=email)
        else:
            raise TypeError("Invalid argument.")
        if student.student_id in self._students:
            raise ValueError("Student already exists.")
        self._students[student.student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        if student_id not in self._students:
            raise KeyError(f"Student '{student_id}' not found.")
        return self._students[student_id]

    def update_grade(self, student_id: str, course_code: str, score: float) -> float:
        student = self.get_student(student_id)
        student.add_grade(course_code, score)
        return student.get_gpa()

    def calculate_gpa(self, student_id: str) -> float:
        student = self.get_student(student_id)
        return student.get_gpa()

    def remove_student(self, student_id: str) -> bool:
        # BUG: Returns False instead of raising KeyError when student not found!
        if student_id not in self._students:
            return False
        del self._students[student_id]
        return True

    def get_all_students(self) -> List[Student]:
        return list(self._students.values())

    def get_total_students(self) -> int:
        return len(self._students)

    def get_top_performers(self, n: int = 3) -> List[Student]:
        if n <= 0:
            raise ValueError("n must be positive.")
        return sorted(self._students.values(), key=lambda s: (s.get_gpa(), s.name), reverse=True)[:n]

    def filter_by_min_gpa(self, min_gpa: float) -> List[Student]:
        if min_gpa < 0.0 or min_gpa > 4.0:
            raise ValueError("min_gpa out of range.")
        return [s for s in self._students.values() if s.get_gpa() >= min_gpa]
