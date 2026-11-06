"""Code under test (don't modify it: write the tests in exercise.py)."""


def is_leap_year(year: int) -> bool:
    """Leap year: divisible by 4, except those divisible by 100 that aren't divisible by 400."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year: int, month: int) -> int:
    """Number of days in the month (1-12). Invalid month → ValueError."""
    if not 1 <= month <= 12:
        raise ValueError(f"invalid month: {month}")
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return 30 if month in (4, 6, 9, 11) else 31
