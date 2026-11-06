"""The walrus operator `:=`. Use it in every function."""

import re  # noqa: F401
from collections.abc import Callable
from typing import IO

PRICE = re.compile(r"\$\s*(\d+(?:\.\d+)?)")


def read_in_chunks(file: IO[str], size: int) -> list[str]:
    """Read the file in chunks of `size` characters until the end.

    Hint: `while (chunk := file.read(size)):`
    """
    raise NotImplementedError("TODO")


def long_lengths(words: list[str], minimum: int) -> list[int]:
    """Lengths of the words longer than minimum, calling len() ONCE per word."""
    raise NotImplementedError("TODO")


def extract_prices(lines: list[str]) -> list[float]:
    """Prices (as float) from the lines that have one in the `PRICE` format
    ("$ 12.50", "$3"). Other lines are ignored.

    >>> extract_prices(["coffee $ 2.5", "no price", "bread $3"])
    [2.5, 3.0]
    """
    raise NotImplementedError("TODO")


def first_ok(attempt: Callable[[], str | None], max_tries: int) -> str | None:
    """Call `attempt()` up to `max_tries` times and return the first result that isn't
    None (or None if none worked).
    """
    raise NotImplementedError("TODO")
