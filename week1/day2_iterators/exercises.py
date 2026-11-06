"""Day 2 — Iterators, generators and itertools.

    uv run pytest week1/day2_iterators
"""

import itertools
from collections import deque
from collections.abc import Iterable, Iterator


class Countdown:
    """Iterable that yields n, n-1, ..., 1.

    It must be iterable MORE THAN ONCE: `__iter__` must return a new
    iterator every time. The simplest way is to make `__iter__` a generator.

    >>> list(Countdown(3))
    [3, 2, 1]
    """

    def __init__(self, n: int) -> None:
        self.n = n

    def __iter__(self) -> Iterator[int]:
        raise NotImplementedError("TODO")


class ManualCounter:
    """Iterator written "by hand" (no generators): yields start, start+1, ...,
    up to `stop` exclusive.

    Implement `__iter__` (returns self) and `__next__` (raises StopIteration
    when done). It is an iterator: it can be consumed only once.
    """

    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self) -> "ManualCounter":
        raise NotImplementedError("TODO")

    def __next__(self) -> int:
        raise NotImplementedError("TODO")


def fibonacci() -> Iterator[int]:
    """Infinite generator: 0, 1, 1, 2, 3, 5, ...

    Try it with `itertools.islice(fibonacci(), 10)`.
    """
    raise NotImplementedError("TODO")


def useful_lines(lines: Iterable[str]) -> Iterator[str]:
    """Yield the lines with surrounding whitespace stripped, skipping empty
    lines and comments (those starting with '#' after the strip).
    """
    raise NotImplementedError("TODO")


def deep_flatten(nested: Iterable[object]) -> Iterator[object]:
    """Flatten nested lists/tuples to any depth.

    Strings are NOT opened up (they are iterable, but are treated as atoms).

    Hint: recursion + `yield from`.

    >>> list(deep_flatten([1, [2, (3, [4])], "ab"]))
    [1, 2, 3, 4, 'ab']
    """
    raise NotImplementedError("TODO")


def in_batches(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Split into tuples of size `n` (the last one may be shorter).

    It must work with iterators (no len or slicing).
    Implement it with `itertools.islice`; then look at `itertools.batched` (3.12+).

    >>> list(in_batches(range(5), 2))
    [(0, 1), (2, 3), (4,)]
    """
    raise NotImplementedError("TODO")


def sliding_windows(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Sliding windows of size `n`.

    Hint: `collections.deque(maxlen=n)`.

    >>> list(sliding_windows([1, 2, 3, 4], 3))
    [(1, 2, 3), (2, 3, 4)]
    """
    raise NotImplementedError("TODO")


def run_length_encode(text: str) -> list[tuple[str, int]]:
    """Run-length encoding of consecutive characters.

    Hint: `itertools.groupby`.

    >>> run_length_encode("aaabcc")
    [('a', 3), ('b', 1), ('c', 2)]
    """
    raise NotImplementedError("TODO")


def combinations_summing_to(nums: list[int], k: int, target: int) -> list[tuple[int, ...]]:
    """All combinations of `k` elements (in itertools order)
    whose sum is `target`.

    Hint: `itertools.combinations`.
    """
    raise NotImplementedError("TODO")


def first_even_squares(numbers: Iterable[int], n: int) -> list[int]:
    """The first `n` even squares from `numbers`.

    `numbers` can be INFINITE (e.g. `itertools.count()`): build a lazy
    pipeline with generator expressions and cut it with `islice`.
    """
    raise NotImplementedError("TODO")
