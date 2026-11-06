"""Names, objects and mutability."""

from decimal import Decimal  # noqa: F401


def append_without_mutating(xs: list[int], x: int) -> list[int]:
    """Return a NEW list with `x` appended at the end. Don't modify `xs`.

    >>> append_without_mutating([1, 2], 3)
    [1, 2, 3]
    """
    raise NotImplementedError("TODO")


def copy_matrix(m: list[list[int]]) -> list[list[int]]:
    """Copy a matrix so that modifying the copy does NOT affect the original
    (neither the rows nor their elements).

    >>> copy_matrix([[1, 2], [3]])
    [[1, 2], [3]]
    """
    raise NotImplementedError("TODO")


def sum_prices(prices: list[str]) -> Decimal:
    """Sum prices given as strings, without float rounding errors.

    >>> sum_prices(["0.10", "0.20"])
    Decimal('0.30')
    """
    raise NotImplementedError("TODO")


def split_evenly(total: int, people: int) -> tuple[int, int]:
    """Return (how much each person gets, how much is left over) using integer division.

    The result must satisfy `each * people + leftover == total`.

    >>> split_evenly(17, 5)
    (3, 2)
    """
    raise NotImplementedError("TODO")
