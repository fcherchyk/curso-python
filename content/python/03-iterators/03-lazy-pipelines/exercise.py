"""Lazy pipelines."""

import itertools  # noqa: F401
from collections.abc import Iterable, Iterator


def first_even_squares(numbers: Iterable[int], n: int) -> list[int]:
    """The first `n` even squares from `numbers`.

    `numbers` may be INFINITE (e.g. `itertools.count()`): build a lazy
    pipeline with generator expressions and cut it with `islice`.

    >>> first_even_squares(range(1, 100), 3)
    [4, 16, 36]
    """
    raise NotImplementedError("TODO")


def in_batches(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Split into tuples of size `n` (the last one may be shorter).

    It must work with lists and with infinite iterators (no len or slicing),
    and be lazy. Implement it with `islice` (don't use `itertools.batched`).

    >>> list(in_batches(range(5), 2))
    [(0, 1), (2, 3), (4,)]
    """
    raise NotImplementedError("TODO")


def parse_access_log(lines: Iterable[str]) -> Iterator[tuple[str, int, int]]:
    """Generator that parses log lines in the format `IP METHOD PATH STATUS BYTES`
    and yields (ip, status, bytes) tuples.

    Skip malformed lines (number of fields other than 5, or invalid numbers).

    >>> list(parse_access_log(["1.1.1.1 GET / 200 512", "garbage"]))
    [('1.1.1.1', 200, 512)]
    """
    raise NotImplementedError("TODO")


def bytes_by_status(lines: Iterable[str]) -> dict[int, int]:
    """Total bytes per status code, iterating over the lines only ONCE.

    Reuse `parse_access_log` as a pipeline stage. Return the keys sorted.

    >>> bytes_by_status(["a GET / 200 10", "b GET / 500 5", "c GET / 200 1"])
    {200: 11, 500: 5}
    """
    raise NotImplementedError("TODO")
