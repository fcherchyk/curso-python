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
    current = start - 1

    def next_value() -> int:
        nonlocal current
        current += 1
        return current

    return next_value


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Right-to-left composition: compose(f, g, h)(x) == f(g(h(x))).

    With no functions, return the identity.

    Hint: `functools.reduce`.
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: counts the calls in the wrapper's `.calls` attribute.

    It must preserve the original function's `__name__` and `__doc__`
    (hint: `functools.wraps`).
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.calls += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)

    wrapper.calls = 0  # type: ignore[attr-defined]
    return wrapper


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

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
            raise AssertionError("unreachable")

        return wrapper

    return decorator


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Simple cache decorator keyed by positional (hashable) arguments.

    Implement it yourself with a dict (in real life: `functools.cache`).
    Expose the dict as the wrapper's `.cache` attribute.
    """
    cache: dict[tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper


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
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.duration = time.perf_counter() - self._start


@contextmanager
def in_directory(path: str | Path) -> Iterator[Path]:
    """Change the working directory for the duration of the block and restore it
    on exit, EVEN if there is an exception. Yields the new directory as a Path.

    Hint: `@contextmanager` + try/finally around the `yield`.
    """
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(previous)


@contextmanager
def capture_errors(*error_types: type[Exception]) -> Iterator[list[Exception]]:
    """Suppress exceptions of the given `error_types` and append them to the list
    the `with` hands you. Any others propagate.

        with capture_errors(ValueError) as errors:
            int("x")
        errors  # [ValueError(...)]
    """
    errors: list[Exception] = []
    try:
        yield errors
    except error_types as e:
        errors.append(e)
