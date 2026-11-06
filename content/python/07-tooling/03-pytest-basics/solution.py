"""Reference tests for business_calendar.py."""

import pytest
from business_calendar import days_in_month, is_leap_year


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        pytest.param(2024, True, id="divisible-by-4"),
        pytest.param(2023, False, id="common"),
        pytest.param(1900, False, id="non-leap-century"),
        pytest.param(2000, True, id="divisible-by-400"),
    ],
)
def test_is_leap_year(year, expected):
    assert is_leap_year(year) is expected


@pytest.mark.parametrize(
    ("month", "days"),
    [(1, 31), (4, 30), (6, 30), (9, 30), (11, 30), (12, 31)],
)
def test_days_of_non_february_months(month, days):
    assert days_in_month(2023, month) == days


def test_february():
    assert days_in_month(2024, 2) == 29
    assert days_in_month(2023, 2) == 28
    assert days_in_month(1900, 2) == 28


@pytest.mark.parametrize("month", [0, 13, -1])
def test_invalid_month(month):
    with pytest.raises(ValueError, match="invalid month"):
        days_in_month(2024, month)
