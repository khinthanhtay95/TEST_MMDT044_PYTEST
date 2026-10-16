"""Module 3: State Management - Student Management System

This module provides classes for managing students, course grades, and GPAs.
Students must write unit tests using fixtures, state transition tracking,
and edge case assertions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Student:
    """Represents an individual student record."""
    student_id: str
    name: str
    email: str
    grades: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if not self.student_id or not isinstance(self.student_id, str):
            raise ValueError("student_id must be a non-empty string.")
        if not self.name or not isinstance(self.name, str):
            raise ValueError("name must be a non-empty string.")
        if not self.email or not isinstance(self.email, str) or "@" not in self.email:
            raise ValueError("email must be a valid non-empty email string.")

    def add_grade(self, course_code: str, score: float) -> None:
        """Add or update a course numeric grade (0.0 to 100.0)."""
        if not course_code or not isinstance(course_code, str):
            raise ValueError("course_code must be a non-empty string.")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Score must be numeric.")
        if score < 0.0 or score > 100.0:
            raise ValueError(f"Score {score} out of range [0.0, 100.0].")
        self.grades[course_code] = float(score)

    def get_gpa(self) -> float:
        """Calculate GPA on a 4.0 scale based on standard course grade conversions.

        Grade scale:
        - score >= 90.0: 4.0
        - score >= 80.0: 3.0
        - score >= 70.0: 2.0
        - score >= 60.0: 1.0
        - score < 60.0:  0.0

        Returns 0.0 if no grades have been recorded.
        """
        if not self.grades:
            return 0.0
        
        points = []
        for score in self.grades.values():
            if score >= 90.0:
                points.append(4.0)
            elif score >= 80.0:
                points.append(3.0)
            elif score >= 70.0:
                points.append(2.0)
            elif score >= 60.0:
                points.append(1.0)
            else:
                points.append(0.0)
                
        return round(sum(points) / len(points), 2)


class StudentManager:
    """Manages collection of student records and operations."""

    def __init__(self):
        self._students: Dict[str, Student] = {}

    def add_student(self, student_or_id, name: Optional[str] = None, email: Optional[str] = None) -> Student:
        """Add a student to the manager.

        Can be called with a `Student` instance or with individual arguments (id, name, email).

        Raises:
            ValueError: If student_id already exists.
            TypeError: If input types are invalid.
        """
        if isinstance(student_or_id, Student):
            student = student_or_id
        elif isinstance(student_or_id, str):
            if name is None or email is None:
                raise ValueError("name and email must be provided when passing student_id.")
            student = Student(student_id=student_or_id, name=name, email=email)
        else:
            raise TypeError("Invalid argument for add_student.")

        if student.student_id in self._students:
            raise ValueError(f"Student with ID '{student.student_id}' already exists.")

        self._students[student.student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        """Retrieve student record by student_id.

        Raises:
            KeyError: If student_id is not found.
        """
        if student_id not in self._students:
            raise KeyError(f"Student '{student_id}' not found.")
        return self._students[student_id]

    def update_grade(self, student_id: str, course_code: str, score: float) -> float:
        """Add or update grade for a student in a course.

        Returns updated GPA for the student.

        Raises:
            KeyError: If student_id not found.
            ValueError / TypeError: If course or score is invalid.
        """
        student = self.get_student(student_id)
        student.add_grade(course_code, score)
        return student.get_gpa()

    def calculate_gpa(self, student_id: str) -> float:
        """Calculate and return student's GPA.

        Raises:
            KeyError: If student_id not found.
        """
        student = self.get_student(student_id)
        return student.get_gpa()

    def remove_student(self, student_id: str) -> bool:
        """Remove a student by ID.

        Returns True if successful.

        Raises:
            KeyError: If student_id not found.
        """
        if student_id not in self._students:
            raise KeyError(f"Student '{student_id}' not found.")
        del self._students[student_id]
        return True

    def get_all_students(self) -> List[Student]:
        """Return list of all registered students."""
        return list(self._students.values())

    def get_total_students(self) -> int:
        """Return count of registered students."""
        return len(self._students)

    def get_top_performers(self, n: int = 3) -> List[Student]:
        """Return the top n students ordered by GPA descending.

        Raises:
            ValueError: If n <= 0.
        """
        if n <= 0:
            raise ValueError("n must be a positive integer.")
        sorted_students = sorted(
            self._students.values(),
            key=lambda s: (s.get_gpa(), s.name),
            reverse=True
        )
        return sorted_students[:n]

    def filter_by_min_gpa(self, min_gpa: float) -> List[Student]:
        """Return all students whose GPA is >= min_gpa."""
        if min_gpa < 0.0 or min_gpa > 4.0:
            raise ValueError("min_gpa must be between 0.0 and 4.0.")
        return [s for s in self._students.values() if s.get_gpa() >= min_gpa]
