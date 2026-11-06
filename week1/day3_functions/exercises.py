"""Day 3 — First-class functions, closures, decorators and context managers.

    uv run pytest week1/day3_functions
"""

import functools
import os
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a function that, each time it is called, returns the next
    integer starting at `start`.

    Hint: closure + `nonlocal`.

    >>> c = make_counter(5)
    >>> c(), c()
    (5, 6)
    """
    raise NotImplementedError("TODO")


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Right-to-left composition: compose(f, g, h)(x) == f(g(h(x))).

    With no functions, return the identity.

    Hint: `functools.reduce`.
    """
    raise NotImplementedError("TODO")


def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: counts the calls in the wrapper's `.calls` attribute.

    It must preserve the original function's `__name__` and `__doc__`
    (hint: `functools.wraps`).
    """
    raise NotImplementedError("TODO")


def retry(
    times: int, exceptions: tuple[type[BaseException], ...] = (Exception,)
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator factory: retries the function up to `times` attempts in
    total if it raises one of `exceptions`. If the attempts run out,
    re-raise the last exception. Other exceptions propagate immediately.

    Usage:
        @retry(3, exceptions=(ConnectionError,))
        def call_api(): ...

    Hint: three levels of functions (factory -> decorator -> wrapper).
    """
    raise NotImplementedError("TODO")


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Simple cache decorator keyed by positional (hashable) arguments.

    Implement it yourself with a dict (in real life: `functools.cache`).
    Expose the dict as the wrapper's `.cache` attribute.
    """
    raise NotImplementedError("TODO")


class Timer:
    """Context manager that measures how long the block takes.

        with Timer() as t:
            do_something()
        print(t.duration)   # seconds (float)

    Use `time.perf_counter()`. `duration` is None until the block finishes.
    It does not suppress exceptions.
    """

    def __init__(self) -> None:
        self.duration: float | None = None
        self._start = 0.0

    def __enter__(self) -> "Timer":
        raise NotImplementedError("TODO")

    def __exit__(self, *exc_info: object) -> None:
        raise NotImplementedError("TODO")


@contextmanager
def in_directory(path: str | Path) -> Iterator[Path]:
    """Change the working directory for the duration of the block and restore it
    on exit, EVEN if there is an exception. Yields the new directory as a Path.

    Hint: `@contextmanager` + try/finally around the `yield`.
    """
    raise NotImplementedError("TODO")


@contextmanager
def capture_errors(*error_types: type[Exception]) -> Iterator[list[Exception]]:
    """Suppress exceptions of the given `error_types` and append them to the list
    the `with` hands you. Any others propagate.

        with capture_errors(ValueError) as errors:
            int("x")
        errors  # [ValueError(...)]
    """
    raise NotImplementedError("TODO")
