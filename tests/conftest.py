"""Shared pytest fixtures.

pytest loads this file automatically, so test files can use these fixtures
just by naming them as function arguments (no import needed).
Every fixture uses the default "function" scope: each test gets a brand-new
object, so one test can never change the data another test sees.
"""

import pytest

from src.student_manager import Student, StudentManager

@pytest.fixture
def empty_manager():
    return StudentManager()

@pytest.fixture
def sample_student():
    """A studentManager holding 4 students, each in a diff GPA band.
    Grade scale : >=90 ->> 4.0,  >=80 ->> 3.0,  >=70 ->> 2.0,  >=60 ->> 1.0, <60 ->> 0.0"""
    return Student(student_id="S001", name="Aung Aung", email="aung.aung@mmdt.edu")

@pytest.fixture
def populated_manager(empty_manager):
    roster = [
        ("S001", "Aung Aung", "aung.aung@mmdt.edu", {"AI101": 95, "ML201": 92}),
        ("S002", "Hla Hla",   "hla.hla@mmdt.edu",   {"AI101": 88, "ML201": 81}),
        ("S003", "Mya Mya",   "mya.mya@mmdt.edu",   {"AI101": 85, "ML201": 75}),
        ("S004", "Zaw Zaw",   "zaw.zaw@mmdt.edu",   {"AI101": 65, "ML201": 55}),
    ]
    for student_id, name, email, grades in roster:
        empty_manager.add_student(student_id, name, email)
        for course_code, score in grades.items():
            empty_manager.update_grade(student_id, course_code, score)
    return empty_manager

@pytest.fixture
def expected_gpas():
    return {"S001": 4.0, "S002": 3.0, "S003": 2.5, "S004": 0.5}

@pytest.fixture
def valid_registration_data():
    return {
        "username": "krystal_01",
        "email": "krystal.htay+mmdt@student.example.com",
        "password": "Secure#2026",
        "age": 25,
    }
