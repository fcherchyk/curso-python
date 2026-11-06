"""itertools: the building blocks."""

import itertools  # noqa: F401
from collections import deque  # noqa: F401
from collections.abc import Iterable, Iterator


def windows(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Sliding windows of size `n`. It must be lazy.

    Hint: `collections.deque(maxlen=n)`.

    >>> list(windows([1, 2, 3, 4], 3))
    [(1, 2, 3), (2, 3, 4)]
    """
    raise NotImplementedError("TODO")


def compress_runs(text: str) -> list[tuple[str, int]]:
    """Run-length encoding of consecutive characters.

    Hint: `itertools.groupby`.

    >>> compress_runs("aaabccaa")
    [('a', 3), ('b', 1), ('c', 2), ('a', 2)]
    """
    raise NotImplementedError("TODO")


def combinations_that_sum(nums: list[int], k: int, target: int) -> list[tuple[int, ...]]:
    """All combinations of `k` elements (in itertools order) whose sum
    is `target`.

    >>> combinations_that_sum([1, 2, 3, 4, 5], 2, 6)
    [(1, 5), (2, 4)]
    """
    raise NotImplementedError("TODO")


def balances(initial: float, transactions: Iterable[float]) -> list[float]:
    """Balance after each transaction, starting with the initial one.

    Hint: `itertools.accumulate(..., initial=...)`.

    >>> balances(1000, [100, -30, 50])
    [1000, 1100, 1070, 1120]
    """
    raise NotImplementedError("TODO")
