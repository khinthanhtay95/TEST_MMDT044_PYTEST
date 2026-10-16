"""Calculator mutants with intentional bugs."""
import math
from typing import List, Union


# Mutant 1: is_prime treats 1 as prime
def is_prime_mutant_1(n: int) -> bool:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 1:  # BUG: treats 1 as prime!
        return False
    if n in (1, 2, 3):
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


# Mutant 2: calculate_average returns 0.0 instead of raising ValueError on empty list
def calculate_average_mutant_2(scores: List[Union[int, float]]) -> float:
    if not isinstance(scores, (list, tuple)):
        raise TypeError("Scores must be provided as a list or tuple.")
    if len(scores) == 0:
        return 0.0  # BUG: returns 0.0 instead of raising ValueError!
    total = 0.0
    for score in scores:
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("Invalid score element.")
        if score < 0 or score > 100:
            raise ValueError("Score out of bounds.")
        total += float(score)
    return round(total / len(scores), 2)


# Mutant 3: find_maximum initializes max to 0, failing on lists of all negative numbers
def find_maximum_mutant_3(numbers: List[Union[int, float]]) -> Union[int, float]:
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("Numbers must be provided as a list or tuple.")
    if len(numbers) == 0:
        raise ValueError("Numbers list cannot be empty.")
    max_val = 0  # BUG: initializes to 0 instead of numbers[0] or None!
    for num in numbers:
        if isinstance(num, bool) or not isinstance(num, (int, float)):
            raise TypeError("Invalid element.")
        if num > max_val:
            max_val = num
    return max_val
