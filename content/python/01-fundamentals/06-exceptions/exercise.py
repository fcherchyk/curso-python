"""Exceptions."""

from pathlib import Path


def to_int(text: str, default: int | None = None) -> int | None:
    """Convert `text` to int (surrounding whitespace is allowed). If that's not possible,
    return `default`. Use EAFP (try/except), not `isdigit`.

    >>> to_int(" 42 ")
    42
    >>> to_int("4.2", default=-1)
    -1
    """
    raise NotImplementedError("TODO")


class InsufficientFunds(Exception):
    """Fill in: store `balance` and `amount` as attributes and build a message
    that includes both values."""

    def __init__(self, balance: float, amount: float) -> None:
        raise NotImplementedError("TODO")


def withdraw(balance: float, amount: float) -> float:
    """Return the balance after withdrawing `amount`.

    - amount <= 0 → ValueError
    - amount > balance → InsufficientFunds(balance, amount)
    """
    raise NotImplementedError("TODO")


class ConfigError(Exception):
    pass


def read_config(path: Path) -> dict[str, str]:
    """Read a file of `key=value` lines (skip empty ones) and return a dict.

    If the file doesn't exist, raise ConfigError chained to the original
    FileNotFoundError (`raise ... from e`).
    """
    raise NotImplementedError("TODO")


def process_all(texts: list[str]) -> tuple[list[int], list[str]]:
    """Convert each text to int. Don't stop at the first error: return
    (converted numbers, texts that failed), in order.

    >>> process_all(["1", "x", "3"])
    ([1, 3], ['x'])
    """
    raise NotImplementedError("TODO")
