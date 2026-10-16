"""Module 1: Basic Functions - Calculator

This module provides basic mathematical and statistical functions.
Students must write unit tests to verify standard behavior, boundary conditions,
type safety, and exception handling.
"""

from typing import List, Union
import math


def calculate_average(scores: List[Union[int, float]]) -> float:
    """Calculate the arithmetic mean of a list of exam scores.

    Specifications:
    - `scores` must be a non-empty list or tuple of numeric values (int or float).
    - Each score must be within the valid range [0, 100].
    - Returns the average rounded to 2 decimal places.

    Raises:
        TypeError: If `scores` is not a list or tuple, or contains non-numeric items.
        ValueError: If `scores` is empty, or if any score is < 0 or > 100.
    """
    if not isinstance(scores, (list, tuple)):
        raise TypeError("Scores must be provided as a list or tuple.")
    if len(scores) == 0:
        raise ValueError("Scores list cannot be empty.")
    
    total = 0.0
    for score in scores:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError(f"Invalid score element: {score}. All elements must be numeric.")
        if score < 0 or score > 100:
            raise ValueError(f"Score {score} out of valid bounds [0, 100].")
        total += float(score)
    
    return round(total / len(scores), 2)


def find_maximum(numbers: List[Union[int, float]]) -> Union[int, float]:
    """Find the maximum number in a list.

    Specifications:
    - `numbers` must be a non-empty list or tuple of numeric values (int or float).
    - Returns the largest value in `numbers`.

    Raises:
        TypeError: If `numbers` is not a list or tuple, or contains non-numeric items.
        ValueError: If `numbers` is empty.
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("Numbers must be provided as a list or tuple.")
    if len(numbers) == 0:
        raise ValueError("Numbers list cannot be empty.")
    
    max_val = None
    for num in numbers:
        if isinstance(num, bool) or not isinstance(num, (int, float)):
            raise TypeError(f"Invalid element: {num}. All elements must be numeric.")
        if max_val is None or num > max_val:
            max_val = num
            
    return max_val


def is_prime(n: int) -> bool:
    """Determine whether an integer n is a prime number.

    Specifications:
    - `n` must be an integer.
    - Numbers <= 1 are NOT prime.
    - 2 and 3 are prime.
    - Even numbers > 2 are NOT prime.
    - Returns True if `n` is prime, False otherwise.

    Raises:
        TypeError: If `n` is not an integer (or is a boolean).
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    limit = math.isqrt(n)
    i = 5
    while i <= limit:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
        
    return True


def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer n.

    Specifications:
    - `n` must be a non-negative integer.
    - 0! = 1.
    - Returns n!

    Raises:
        TypeError: If `n` is not an integer (or is a boolean).
        ValueError: If `n` is negative.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    if n in (0, 1):
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def power(base: Union[int, float], exponent: int) -> Union[int, float]:
    """Calculate base raised to the power of exponent.

    Specifications:
    - `base` must be numeric (int or float).
    - `exponent` must be an integer.
    - If `base == 0` and `exponent < 0`, raises ValueError (division by zero).

    Raises:
        TypeError: If `base` is not numeric or `exponent` is not integer.
        ValueError: If 0 is raised to a negative power.
    """
    if isinstance(base, bool) or not isinstance(base, (int, float)):
        raise TypeError("Base must be numeric.")
    if isinstance(exponent, bool) or not isinstance(exponent, int):
        raise TypeError("Exponent must be an integer.")
    if base == 0 and exponent < 0:
        raise ValueError("Cannot raise zero to a negative power.")
    
    return base ** exponent
