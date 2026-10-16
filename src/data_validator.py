"""Module 2: Data Validation - Validator

This module provides data validation rules and custom exceptions for user registration.
Students must write unit tests to verify valid data, rejection of malformed inputs,
and proper exception raising with pytest.raises.
"""

from typing import Dict, Any
import re


class ValidationError(Exception):
    """Base exception for all data validation failures."""
    pass


class InvalidEmailError(ValidationError):
    """Raised when an email address does not conform to valid standard format."""
    pass


class WeakPasswordError(ValidationError):
    """Raised when a password fails complexity or length requirements."""
    pass


class InvalidAgeError(ValidationError):
    """Raised when an age value is outside allowable bounds."""
    pass


class InvalidUsernameError(ValidationError):
    """Raised when a username does not meet formatting constraints."""
    pass


def validate_email(email: str) -> bool:
    """Validate an email address string.

    Specifications:
    - Must be a string.
    - Format: <local_part>@<domain>.<extension>
    - Local part: letters, digits, and dots/underscores/hyphens/plus (no consecutive dots).
    - Domain: alphanumeric and hyphens.
    - Extension: alphabetic characters with length >= 2.
    - No leading, trailing, or internal whitespace.

    Raises:
        TypeError: If email is not a string.
        InvalidEmailError: If format is invalid or empty.
    """
    if not isinstance(email, str):
        raise TypeError("Email must be a string.")
    
    email = email.strip()
    if not email:
        raise InvalidEmailError("Email cannot be empty.")
    
    pattern = r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    if ".." in email or not re.match(pattern, email):
        raise InvalidEmailError(f"'{email}' is not a valid email address.")
    
    return True


def validate_password(password: str) -> bool:
    """Validate a password according to standard security rules.

    Specifications:
    - Must be a string.
    - Minimum length: 8 characters.
    - Maximum length: 128 characters.
    - Must contain at least one uppercase letter [A-Z].
    - Must contain at least one lowercase letter [a-z].
    - Must contain at least one digit [0-9].
    - Must contain at least one special character from: !@#$%^&*()_+-=[]{}|;:,.<>?
    - Must not contain any whitespace characters.

    Raises:
        TypeError: If password is not a string.
        WeakPasswordError: If any criteria is violated.
    """
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
    
    special_chars = set("!@#$%^&*()_+-=[]{}|;:,.<>?")
    if not any(c in special_chars for c in password):
        raise WeakPasswordError("Password must contain at least one special character.")
    
    return True


def validate_username(username: str) -> bool:
    """Validate a user handle / username.

    Specifications:
    - Must be a string between 3 and 20 characters inclusive.
    - Must start with an alphabetic character [a-zA-Z].
    - May contain letters, digits, and underscores.
    - No spaces or special symbols allowed.

    Raises:
        TypeError: If username is not a string.
        InvalidUsernameError: If constraints are violated.
    """
    if not isinstance(username, str):
        raise TypeError("Username must be a string.")
    
    if len(username) < 3 or len(username) > 20:
        raise InvalidUsernameError("Username must be between 3 and 20 characters in length.")
    
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
        raise InvalidUsernameError("Username must start with a letter and contain only alphanumeric characters and underscores.")
    
    return True


def validate_age(age: int) -> bool:
    """Validate a user's age.

    Specifications:
    - Must be an integer (boolean types rejected).
    - Minimum age: 13 (COPPA compliance limit).
    - Maximum age: 120.

    Raises:
        TypeError: If age is not an integer or is boolean.
        InvalidAgeError: If age < 13 or age > 120.
    """
    if isinstance(age, bool) or not isinstance(age, int):
        raise TypeError("Age must be an integer.")
    
    if age < 13:
        raise InvalidAgeError("Age must be at least 13 years old.")
    if age > 120:
        raise InvalidAgeError("Age must not exceed 120 years.")
    
    return True


def validate_registration(data: Dict[str, Any]) -> bool:
    """Validate complete user registration payload dictionary.

    Specifications:
    - `data` must be a dictionary.
    - Required fields: 'username', 'email', 'password', 'age'.
    - Validates each field according to its respective validation function.

    Raises:
        TypeError: If data is not a dict.
        ValidationError: If missing required keys or any individual field validation fails.
    """
    if not isinstance(data, dict):
        raise TypeError("Registration data must be a dictionary.")
    
    required_fields = ["username", "email", "password", "age"]
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Missing required registration field: '{field}'.")
    
    validate_username(data["username"])
    validate_email(data["email"])
    validate_password(data["password"])
    validate_age(data["age"])
    
    return True
