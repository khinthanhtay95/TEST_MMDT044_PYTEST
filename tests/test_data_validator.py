"""Unit tests for src/data_validator.py.

For every validator checking:
  * valid inputs return True
  * each broken rule raises the right custom exception AND the right message
  * wrong input types raise TypeError
Test names contain the validator name (e.g. "validate_email") so that
`pytest -k validate_email` selects exactly the tests for validator.
"""

import pytest

from src.data_validator import (
    InvalidAgeError,
    InvalidEmailError,
    InvalidUsernameError,
    ValidationError,
    WeakPasswordError,
    validate_age,
    validate_email,
    validate_password,
    validate_registration,
    validate_username,
)

# Custom exception hierarchy

@pytest.mark.parametrize(
    "exception_class",
    [InvalidEmailError, WeakPasswordError, InvalidAgeError, InvalidUsernameError],
)
def test_custom_exceptions_inherit_from_validation_error(exception_class):
    assert issubclass(exception_class, ValidationError)
    assert issubclass(ValidationError, Exception)

# validate_email(email)

@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "first.last@example.com",
        "user+newsletter@example.com",      # plus addressing
        "user_name-1@example.org",
        "user@mail.example.com",            # subdomain
        "user@dept.mmdt.example.co.uk",     # several subdomains
        "a@b.io",                           # shortest TLD (2 letters)
        "USER@EXAMPLE.COM",                 # upper case
        "12345@example.net",                # digits only in local part
        "user@my-domain.com",               # hyphen in domain
    ],
)
def test_validate_email_valid_addresses(email):
    assert validate_email(email) is True


def test_validate_email_strips_surrounding_whitespace():
    # The code calls email.strip() first, so outer spaces are allowed.
    assert validate_email("  user@example.com  ") is True


@pytest.mark.parametrize("email", ["", "   ", "\t\n"], ids=["empty", "spaces", "tab_newline"])
def test_validate_email_empty_raises_invalid_email_error(email):
    with pytest.raises(InvalidEmailError, match="cannot be empty"):
        validate_email(email)


@pytest.mark.parametrize(
    "email",
    [
        "userexample.com",          # missing @
        "user@",                    # missing domain
        "@example.com",             # missing local part
        "user@example",             # missing top-level domain
        "user@localhost",           # missing top-level domain
        "user@example.c",           # TLD only 1 letter
        "user@example.123",         # TLD must be letters
        "user..name@example.com",   # consecutive dots in local part
        "user@example..com",        # consecutive dots in domain
        "user name@example.com",    # internal space
        "user@exa mple.com",        # internal space in domain
        "user\t@example.com",       # internal tab
        "user@@example.com",        # double @
        "user@example.com.",        # trailing dot
        "user@example_site.com",    # underscore not allowed in domain
        "user#1@example.com",       # '#' not allowed in local part
    ],
    ids=[
        "no_at", "no_domain", "no_local_part", "no_tld", "localhost", "tld_1_letter",
        "numeric_tld", "double_dot_local", "double_dot_domain", "space_local",
        "space_domain", "tab", "double_at", "trailing_dot", "underscore_domain", "hash_char",
    ],
)
def test_validate_email_invalid_format_raises_invalid_email_error(email):
    with pytest.raises(InvalidEmailError, match="is not a valid email address"):
        validate_email(email)

def test_validate_email_error_is_also_a_validation_error():
    with pytest.raises(ValidationError):
        validate_email("user@example")

@pytest.mark.parametrize("email", [None, 123, ["user@example.com"], b"user@example.com"],
                         ids=["none", "int", "list", "bytes"])
def test_validate_email_non_string_raises_type_error(email):
    with pytest.raises(TypeError, match="Email must be a string"):
        validate_email(email)

# validate_password(password)

SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"

@pytest.mark.parametrize(
    "password",
    [
        "Secure#2026",
        "Abcdef1!",                 # exactly 8 characters (minimum)
        "Aa1!" + "a" * 124,         # exactly 128 characters (maximum)
        "P@ssw0rd",
        "MMDT_test_44",
    ],
    ids=["normal", "min_length_8", "max_length_128", "classic", "underscore_special"],
)
def test_validate_password_strong_passwords(password):
    assert validate_password(password) is True

@pytest.mark.parametrize("special", list(SPECIAL_CHARS))
def test_validate_password_accepts_every_listed_special_character(special):
    assert validate_password("Abcdef1" + special) is True

@pytest.mark.parametrize(
    "password, message",
    [
        ("", "at least 8 characters"),
        ("Abc1!xy", "at least 8 characters"),                                  # 7 chars
        ("Aa1!" + "a" * 125, "exceeds maximum allowable length of 128"),       # 129 chars
        ("Abc 12!x", "must not contain whitespace"),                           # space
        ("Abcd12!\t", "must not contain whitespace"),                          # tab
        ("abcdef1!", "at least one uppercase letter"),
        ("ABCDEF1!", "at least one lowercase letter"),
        ("Abcdefg!", "at least one digit"),
        ("Abcdefg1", "at least one special character"),
        ("Password123", "at least one special character"),
    ],
    ids=[
        "empty", "length_7", "length_129", "space", "tab", "no_uppercase",
        "no_lowercase", "no_digit", "no_special", "no_special_common",
    ],
)
def test_validate_password_weak_passwords_raise_weak_password_error(password, message):
    with pytest.raises(WeakPasswordError, match=message):
        validate_password(password)

@pytest.mark.parametrize("special", ["~", "/", "`", "'", '"', "\\"])
def test_validate_password_unlisted_symbol_does_not_count_as_special(special):
    with pytest.raises(WeakPasswordError, match="at least one special character"):
        validate_password("Abcdef1" + special)

@pytest.mark.parametrize("password", [None, 12345678, ["Abcdef1!"]], ids=["none", "int", "list"])
def test_validate_password_non_string_raises_type_error(password):
    with pytest.raises(TypeError, match="Password must be a string"):
        validate_password(password)

# validate_username(username)

@pytest.mark.parametrize(
    "username",
    ["abc", "abcdefghijklmnopqrst", "krystal_01", "User123", "a_b", "Z99", "x__"],
    ids=["min_length_3", "max_length_20", "underscore_digits", "mixed_case",
         "underscore_middle", "letter_then_digits", "trailing_underscores"],
)
def test_validate_username_valid_usernames(username):
    assert validate_username(username) is True

@pytest.mark.parametrize(
    "username",
    ["", "a", "ab", "a" * 21, "abcdefghijklmnopqrstu"],
    ids=["empty", "length_1", "length_2", "length_21", "length_21_letters"],
)
def test_validate_username_wrong_length_raises_invalid_username_error(username):
    with pytest.raises(InvalidUsernameError, match="between 3 and 20 characters"):
        validate_username(username)

@pytest.mark.parametrize(
    "username",
    ["1user", "_user", "user-name", "user name", "user!", "user.name", "üser", "abc@d"],
    ids=["starts_with_digit", "starts_with_underscore", "hyphen", "space",
         "exclamation", "dot", "non_ascii_letter", "at_sign"],
)
def test_validate_username_bad_format_raises_invalid_username_error(username):
    with pytest.raises(InvalidUsernameError, match="must start with a letter"):
        validate_username(username)

@pytest.mark.parametrize("username", [None, 123, ["abc"]], ids=["none", "int", "list"])
def test_validate_username_non_string_raises_type_error(username):
    with pytest.raises(TypeError, match="Username must be a string"):
        validate_username(username)

# validate_age(age)

@pytest.mark.parametrize("age", [13, 14, 25, 119, 120], ids=lambda a: f"age={a}")
def test_validate_age_valid_ages(age):
    assert validate_age(age) is True

@pytest.mark.parametrize(
    "age, message",
    [
        (12, "at least 13"),
        (0, "at least 13"),
        (-1, "at least 13"),
        (121, "must not exceed 120"),
        (200, "must not exceed 120"),
    ],
    ids=["age=12", "age=0", "age=-1", "age=121", "age=200"],
)
def test_validate_age_out_of_range_raises_invalid_age_error(age, message):
    with pytest.raises(InvalidAgeError, match=message):
        validate_age(age)

@pytest.mark.parametrize(
    "age",
    [13.0, 25.5, "25", None, True, False],
    ids=["float_whole", "float", "string", "none", "bool_true", "bool_false"],
)
def test_validate_age_non_integer_raises_type_error(age):
    with pytest.raises(TypeError, match="Age must be an integer"):
        validate_age(age)

# validate_registration(data)  (uses the valid_registration_data fixture)

def test_validate_registration_valid_payload(valid_registration_data):
    assert validate_registration(valid_registration_data) is True

def test_validate_registration_allows_extra_fields(valid_registration_data):
    valid_registration_data["nickname"] = "kk"
    assert validate_registration(valid_registration_data) is True

def test_validate_registration_does_not_change_input(valid_registration_data):
    before = dict(valid_registration_data)
    validate_registration(valid_registration_data)
    assert valid_registration_data == before

@pytest.mark.parametrize("missing_field", ["username", "email", "password", "age"])
def test_validate_registration_missing_field_raises_validation_error(valid_registration_data, missing_field):
    del valid_registration_data[missing_field]
    with pytest.raises(ValidationError, match=f"Missing required registration field: '{missing_field}'"):
        validate_registration(valid_registration_data)

def test_validate_registration_empty_dict_raises_validation_error():
    with pytest.raises(ValidationError, match="Missing required registration field"):
        validate_registration({})

@pytest.mark.parametrize(
    "field, bad_value, expected_error",
    [
        ("username", "1krystal", InvalidUsernameError),
        ("email", "krystal@example", InvalidEmailError),
        ("password", "weakpass", WeakPasswordError),
        ("age", 12, InvalidAgeError),
        ("age", 121, InvalidAgeError),
    ],
    ids=["bad_username", "bad_email", "weak_password", "age_too_low", "age_too_high"],
)
def test_validate_registration_invalid_field_propagates_specific_error(
    valid_registration_data, field, bad_value, expected_error
):
    valid_registration_data[field] = bad_value
    with pytest.raises(expected_error):
        validate_registration(valid_registration_data)

@pytest.mark.parametrize(
    "field, bad_value",
    [("username", 123), ("email", None), ("password", 12345678), ("age", "25")],
    ids=["username_int", "email_none", "password_int", "age_string"],
)
def test_validate_registration_wrong_field_type_raises_type_error(valid_registration_data, field, bad_value):
    valid_registration_data[field] = bad_value
    with pytest.raises(TypeError):
        validate_registration(valid_registration_data)

def test_validate_registration_checks_username_first(valid_registration_data):
    valid_registration_data["username"] = "1bad"
    valid_registration_data["email"] = "bad-email"
    with pytest.raises(InvalidUsernameError):
        validate_registration(valid_registration_data)

@pytest.mark.parametrize(
    "data",
    [None, [], "username=krystal", [("username", "krystal_01")]],
    ids=["none", "empty_list", "string", "list_of_pairs"],
)
def test_validate_registration_non_dict_raises_type_error(data):
    with pytest.raises(TypeError, match="must be a dictionary"):
        validate_registration(data)