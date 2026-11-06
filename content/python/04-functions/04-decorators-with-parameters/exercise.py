"""Decorators with parameters."""

import functools  # noqa: F401
import warnings  # noqa: F401
from collections.abc import Callable
from typing import Any

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


def repeat(n: int) -> Decorator:
    """The decorated function returns a list with the results of calling it `n` times.

        @repeat(3)
        def f(): ...
        f()  # [r1, r2, r3]
    """
    raise NotImplementedError("TODO")


def retry(
    times: int, exceptions: tuple[type[BaseException], ...] = (Exception,)
) -> Decorator:
    """Retry up to `times` attempts in total if the function raises any of
    `exceptions`. When they run out, re-raise the last one. Other exceptions
    propagate immediately.
    """
    raise NotImplementedError("TODO")


def clamp(minimum: float, maximum: float) -> Decorator:
    """Clamp the function's RESULT to the range [minimum, maximum].

        @clamp(0, 100)
        def percentage(x): return x * 100
        percentage(1.5)  # 100
    """
    raise NotImplementedError("TODO")


def deprecated(func: Callable[..., Any] | None = None, *, replacement: str | None = None) -> Any:
    """Emit a `DeprecationWarning` every time the decorated function is called.

    Works with and without parentheses:
        @deprecated                        -> "old is deprecated"
        @deprecated(replacement="new")     -> "old is deprecated; use new"
    """
    raise NotImplementedError("TODO")
