"""Data Validator mutants with intentional bugs."""
import re
from typing import Dict, Any
from src.data_validator import (
    ValidationError,
    InvalidEmailError,
    WeakPasswordError,
    InvalidAgeError,
    InvalidUsernameError,
)


# Mutant 1: validate_email allows emails missing domain extension (e.g. user@domain)
def validate_email_mutant_1(email: str) -> bool:
    if not isinstance(email, str):
        raise TypeError("Email must be a string.")
    email = email.strip()
    if not email:
        raise InvalidEmailError("Email cannot be empty.")
    # BUG: Accepts emails without top-level domain extension
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})?$"
    if ".." in email or not re.match(pattern, email):
        raise InvalidEmailError(f"'{email}' is not a valid email address.")
    return True


# Mutant 2: validate_password does not check for special characters
def validate_password_mutant_2(password: str) -> bool:
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if len(password) < 8:
        raise WeakPasswordError("Password must be at least 8 characters long.")
    if len(password) > 128:
        raise WeakPasswordError("Password exceeds maximum allowable length of 128 characters.")
    if any(c.isspace() for c in password):
        raise WeakPasswordError("Password must not contain whitespace.")
    if not any(c.isupper() for c in password):
        raise WeakPasswordError("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        raise WeakPasswordError("Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        raise WeakPasswordError("Password must contain at least one digit.")
    # BUG: Skipped special character check!
    return True


# Mutant 3: validate_registration does not check if required fields are missing
def validate_registration_mutant_3(data: Dict[str, Any]) -> bool:
    if not isinstance(data, dict):
        raise TypeError("Registration data must be a dictionary.")
    # BUG: Missing required field check, tries to validate blindly
    if "username" in data:
        pass
    return True
