"""The iteration protocol."""

from collections.abc import Iterable, Iterator


class Countdown:
    """Iterable that yields n, n-1, ..., 1.

    It must be iterable MORE THAN ONCE: `__iter__` has to return a new
    iterator every time.

    >>> list(Countdown(3))
    [3, 2, 1]
    """

    def __init__(self, n: int) -> None:
        self.n = n

    def __iter__(self) -> Iterator[int]:
        raise NotImplementedError("TODO")


class Counter:
    """Hand-written iterator (no generators): yields start, start+1, ...
    up to `stop` (exclusive). It can be consumed only once.

    Implement `__iter__` (returns self) and `__next__` (raises StopIteration when done).
    """

    def __init__(self, start: int, stop: int) -> None:
        raise NotImplementedError("TODO")

    def __iter__(self) -> "Counter":
        raise NotImplementedError("TODO")

    def __next__(self) -> int:
        raise NotImplementedError("TODO")


def first[T](iterable: Iterable[T], default: T | None = None) -> T | None:
    """First element of any iterable (even an infinite one), or `default` if it is empty.

    Hint: `next(iter(...), default)`.

    >>> first(x for x in range(10) if x > 3)
    4
    """
    raise NotImplementedError("TODO")


def totals_and_percentages(amounts: Iterable[float]) -> list[float]:
    """Percentage each amount represents of the total (rounded to 1 decimal).

    Careful! `amounts` may be a generator and you need to iterate over it twice.
    If the total is 0, return a list of zeros.

    >>> totals_and_percentages([1, 1, 2])
    [25.0, 25.0, 50.0]
    """
    raise NotImplementedError("TODO")
