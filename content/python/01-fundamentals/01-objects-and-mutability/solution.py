from decimal import Decimal


def append_without_mutating(xs: list[int], x: int) -> list[int]:
    return [*xs, x]  # or xs + [x]


def copy_matrix(m: list[list[int]]) -> list[list[int]]:
    # Copying each row is enough: ints are immutable.
    return [row.copy() for row in m]


def sum_prices(prices: list[str]) -> Decimal:
    return sum((Decimal(p) for p in prices), Decimal(0))


def split_evenly(total: int, people: int) -> tuple[int, int]:
    return divmod(total, people)
