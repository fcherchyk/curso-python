"""Closures and scopes."""

from collections.abc import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a function that, each time it's called, returns the next integer
    starting at `start`. Each counter is independent.

    Hint: closure + `nonlocal`.

    >>> c = make_counter(5)
    >>> c(), c()
    (5, 6)
    """
    raise NotImplementedError("TODO")


def multipliers(n: int) -> list[Callable[[int], int]]:
    """List of `n` functions: the i-th one multiplies its argument by i.

    Watch out for late binding!

    >>> [f(10) for f in multipliers(3)]
    [0, 10, 20]
    """
    raise NotImplementedError("TODO")


def make_averager() -> Callable[[float], float]:
    """Return a function that accumulates values and returns the average of all
    the values it has received so far.

    >>> avg = make_averager()
    >>> avg(10), avg(20), avg(60)
    (10.0, 15.0, 30.0)
    """
    raise NotImplementedError("TODO")


def make_limiter(max_calls: int) -> Callable[[], bool]:
    """Return a function that returns True the first `max_calls` times it's
    called, and False afterwards (like a simple rate limiter).

    >>> allowed = make_limiter(2)
    >>> allowed(), allowed(), allowed()
    (True, True, False)
    """
    raise NotImplementedError("TODO")
