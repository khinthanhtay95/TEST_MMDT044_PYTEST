"""Unit tests for the calculator module. src/calculator.py

Each test function should cover a specific aspect of the calculator's functionality,
Each function is tested with three kinds of input:
  * normal values      -> correct result
  * boundary values    -> edges of the valid range (0, 1, 100, single item ...)
  * invalid values     -> ValueError / TypeError with the right message
Every test name contains the function name (e.g. "is_prime") so that
`pytest -k is_prime` selects exactly the tests for that function.
Tests should be independent and not rely on the state of other tests.   """

import math
import pytest
from src.calculator import calculate_average, find_maximum, factorial, is_prime, power


#### calculate_average() tests

@pytest.mark.parametrize(
    "scores, expected",
    [
        ([80, 90, 100], 90.0),
        ([70, 85], 77.5),
        ([0], 0.0),                    #lower boundary
        ([100], 100.0),                #upper boundary
        ([0, 100], 50.0),              #both boundary value
        ([88.5, 91.25], 89.88),        #float values, rounded to 2 decimal places
        ([1, 2, 2], 1.67),             #1.666.... round up to 1.67
        ([42], 42.0),                  #single item list
        ((60, 70, 80), 70.0),          # tuple is also accepted
    ],
    ids=[
        "normal values", "two-itmes", "min_0", "max_100", "min_and_max", 
        "floats", "rounding", "single_item", "tuple"],
)
def test_calculate_average_valid_scores(scores, expected):
    result = calculate_average(scores)
    assert result == pytest.approx(expected), f"Expected {expected}, but got {result} for scores {scores}"

def test_calculate_average_returns_float():
    assert isinstance(calculate_average([90, 80]), float)

def test_calculate_average_empty_list_raises_value_error():
    with pytest.raises(ValueError, match="Scores list cannot be empty."):
        calculate_average([])

def test_calculate_average_empty_tuple_raises_value_error():
    with pytest.raises(ValueError, match="Scores list cannot be empty."):
        calculate_average(())

@pytest.mark.parametrize(
    "scores",
    [[-1], [101], [-0.01], [100.01], [50, 101], [float("inf")]],
    ids=["negative", "above_100", "negative_float", "above_100_float", "mixed_invalid", "infinity"],
)

def test_calculate_average_out_of_bounds_raises_value_error(scores):
    with pytest.raises(ValueError, match="out of valid bounds"):
        calculate_average(scores)

@pytest.mark.parametrize(
    "scores",
    ["90", 90, None, {"math": 90}, {90, 80}, ""],
    ids=["string", "int", "none", "dict", "set", "empty_string"],
)
def test_calculate_average_non_list_raises_type_error(scores):
    with pytest.raises(TypeError, match="list or tuple"):
        calculate_average(scores)

@pytest.mark.parametrize(
    "scores",
    [["90"], [None], [True], [90, False], [[90]]],
    ids=["string_item", "none_item", "bool_true", "bool_false", "nested_list"],
)
def test_calculate_average_non_numeric_item_raises_type_error(scores):
    with pytest.raises(TypeError, match="must be numeric"):
        calculate_average(scores)


######## find_maximum(numbers) tests

@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 5, 3], 5),
        ([-5, -2, -9], -2),          # all negative: max is below 0
        ([-1], -1),                  # single negative item
        ([-3, 0, 2.5], 2.5),         # mixed signs and a float
        ([7, 7, 3], 7),              # duplicate maximum
        ([0, 0, 0], 0),
        ([42], 42),                  # single item
        ([1.5, 1.25, 1.75], 1.75),   # floats only
        ((3, 9, 1), 9),              # tuple is also accepted
        ([10**12, 10**12 + 1], 10**12 + 1),  # very large integers
    ],
    ids=["positive", "all_negative", "single_negative", "mixed", "duplicate_max",
         "all_zero", "single_item", "floats", "tuple", "large_ints"],
)

def test_find_maximum_valid_numbers(numbers, expected):
    result = find_maximum(numbers)
    assert result == expected, f"Expected {expected}, but got {result} for numbers {numbers}"

def test_find_maximum_keeps_integer_type():
    result = find_maximum([3, 8, 1])
    assert result == 8 and isinstance(result, int)

def test_find_maximum_does_not_change_input_list():
    numbers = [4,9,2]
    find_maximum(numbers)
    assert numbers == [4,9,2]

@pytest.mark.parametrize("numbers", [[], ()], ids=["empty_list", "empty_tuple"])
def test_find_maximum_empty_raises_value_error(numbers):
    with pytest.raises(ValueError, match="cannot be empty"):
        find_maximum(numbers)

@pytest.mark.parametrize("numbers", ["123", 5, None, {1, 2}], ids=["string", "int", "none", "set"])
def test_find_maximum_non_list_raises_type_error(numbers):
    with pytest.raises(TypeError, match="list or tuple"):
        find_maximum(numbers)

@pytest.mark.parametrize(
    "numbers",
    [[1, "2"], [None], [True, 2], [1, [2]]],
    ids=["string_item", "none_item", "bool_item", "nested_list"],
)

def test_find_maximum_non_numeric_item_raises_type_error(numbers):
    with pytest.raises(TypeError, match="must be numeric"):
        find_maximum(numbers)


### is_prime(n) tests

@pytest.mark.parametrize("n", [-17, -2, -1, 0, 1], ids=lambda n: f"n={n}")
def test_is_prime_number_less_than_or_equal_to_one_are_not_prime(n):
    assert is_prime(n) is False, f"{n} should not be prime"

@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13], ids=lambda n: f"n={n}")
def test_is_prime_small_primes(n):
    assert is_prime(n) is True, f"{n} must be prime"

@pytest.mark.parametrize("n", [4, 6, 8, 10, 100, 1024], ids=lambda n: f"n={n}")
def test_is_prime_even_numbers_above_two_are_not_prime(n):
    assert is_prime(n) is False, f"{n} is even, so it must not be prime"

@pytest.mark.parametrize(
    "n",
    [9, 15, 21, 25, 35, 49, 77, 121, 169, 1_000_001],
    ids=lambda n: f"n={n}",
)

def test_is_prime_odd_composites_are_not_prime(n):
    # 25, 49, 121, 169 are squares of primes: they check the loop limit sqrt(n)
    # 35 = 5*7 and 77 = 7*11 check the (i + 2) divisor; 1_000_001 = 101 * 9901
    assert is_prime(n) is False, f"{n} is composite, so it must not be prime"

@pytest.mark.parametrize("n", [29, 97, 101, 997, 7919], ids=lambda n: f"n={n}")
def test_is_prime_large_primes(n):
    assert is_prime(n) is True, f"{n} must be prime"

def test_is_prime_matches_trial_division_up_to_200():
    """Compare against a simple, obviously-correct reference for every n."""
    def reference(n):
        return n > 1 and all(n % d != 0 for d in range(2, n))

    wrong = [n for n in range(-5, 201) if is_prime(n) != reference(n)]
    assert wrong == [], f"is_prime gives the wrong answer for: {wrong}"

@pytest.mark.parametrize(
    "n",
    [7.0, 2.5, "7", None, True, False],
    ids=["float_whole", "float", "string", "none", "bool_true", "bool_false"],
)
def test_is_prime_non_integer_raises_type_error(n):
    with pytest.raises(TypeError, match="must be an integer"):
        is_prime(n)


#factorial(n)

@pytest.mark.parametrize(
    "n, expected",
    [(0, 1), (1, 1), (2, 2), (5, 120), (10, 3_628_800), (20, 2_432_902_008_176_640_000)],
    ids=lambda v: str(v),
)
def test_factorial_valid_values(n, expected):
    result = factorial(n)
    assert result == expected, f"{n}! should be {expected}"

def test_factorial_matches_math_factorial_up_to_30():
    for n in range(31):
        assert factorial(n) == math.factorial(n), f"{n}! should match math.factorial"

@pytest.mark.parametrize("n", [-1, -10], ids=lambda n: f"n={n}")
def test_factorial_negative_raises_value_error(n):
    with pytest.raises(ValueError, match="not defined for negative"):
        factorial(n)

@pytest.mark.parametrize(
    "n",
    [3.0, 2.5, "5", None, True, False],
    ids=["float_whole", "float", "string", "none", "bool_true", "bool_false"],
)
def test_factorial_non_integer_raises_type_error(n):
    with pytest.raises(TypeError, match="must be an integer"):
        factorial(n)


##### power(base, exponent) tests

@pytest.mark.parametrize(
    "base, exponent, expected",
    [
        (2, 3, 8),          # positive exponent
        (5, 1, 5),
        (5, 0, 1),          # zero exponent
        (0, 0, 1),          # Python defines 0 ** 0 as 1
        (0, 5, 0),          # zero base, positive exponent
        (2, -1, 0.5),       # negative exponent
        (2, -2, 0.25),
        (10, -3, 0.001),
        (-2, 3, -8),        # negative base, odd exponent
        (-2, 2, 4),         # negative base, even exponent
        (1.5, 2, 2.25),     # float base
    ],
    ids=[
        "2^3", "5^1", "5^0", "0^0", "0^5", "2^-1", "2^-2", "10^-3",
         "neg_odd", "neg_even", "float_base"],
)
def test_power_valid_values(base, exponent, expected):
    result = power(base, exponent)
    assert result == pytest.approx(expected), f"{base}^{exponent} should be {expected}, got {result}"

@pytest.mark.parametrize(
    "base, exponent",
    [(0, -1), (0, -5), (0.0, -2)],
    ids=["int_zero", "int_zero_big", "float_zero"],
)
def test_power_zero_to_negative_exponent_raises_value_error(base, exponent):
    with pytest.raises(ValueError, match="zero to a negative power"):
        power(base, exponent)

@pytest.mark.parametrize("base", ["2", None, True, [2]], ids=["string", "none", "bool", "list"])
def test_power_non_numeric_base_raises_type_error(base):
    with pytest.raises(TypeError, match="Base must be numeric"):
        power(base, 2)

@pytest.mark.parametrize("exponent", [2.0, 0.5, "2", None, True], ids=["float_whole", "float", "string", "none", "bool"])
def test_power_non_integer_exponent_raises_type_error(exponent):
    with pytest.raises(TypeError, match="Exponent must be an integer"):
        power(2, exponent)
