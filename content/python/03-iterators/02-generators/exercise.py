"""Generators.

Every function must be a GENERATOR (use `yield`), not return a list.
"""

from collections.abc import Iterable, Iterator


def fibonacci() -> Iterator[int]:
    """Infinite generator: 0, 1, 1, 2, 3, 5, ...

    Try it with `itertools.islice(fibonacci(), 10)`.
    """
    raise NotImplementedError("TODO")


def useful_lines(lines: Iterable[str]) -> Iterator[str]:
    """Yield the lines stripped of surrounding whitespace, skipping empty ones and
    comments (lines that start with '#' after stripping).
    """
    raise NotImplementedError("TODO")


def deep_flatten(nested: Iterable[object]) -> Iterator[object]:
    """Flatten lists and tuples nested to any depth.

    Strings are NOT opened up (they are iterable, but are treated as atoms).

    Hint: recursion + `yield from`.

    >>> list(deep_flatten([1, [2, (3, [4])], "ab"]))
    [1, 2, 3, 4, 'ab']
    """
    raise NotImplementedError("TODO")


def decimal_range(start: float, stop: float, step: float) -> Iterator[float]:
    """Like `range` but with floats: start, start+step, ... while < stop.

    To avoid accumulating rounding error, compute each value as `start + i * step`
    and round to 10 decimals. If step <= 0, raise ValueError (when next is called!).

    >>> list(decimal_range(0, 0.5, 0.1))
    [0.0, 0.1, 0.2, 0.3, 0.4]
    """
    raise NotImplementedError("TODO")
