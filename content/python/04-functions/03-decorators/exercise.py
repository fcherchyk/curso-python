"""Decorators."""

import functools  # noqa: F401
from collections.abc import Callable
from typing import Any


def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: counts calls in the wrapper's `.calls` attribute.

    It must preserve the original function's `__name__` and `__doc__` and return
    its result.
    """
    raise NotImplementedError("TODO")


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """Cache decorator keyed by positional (hashable) arguments.

    Implement it yourself with a dict (in real life: `functools.cache`).
    Expose the dict as the wrapper's `.cache` attribute.
    """
    raise NotImplementedError("TODO")


HANDLERS: dict[str, Callable[..., Any]] = {}


def handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Registration decorator: stores the function in HANDLERS keyed by its name
    and returns it WITHOUT wrapping.
    """
    raise NotImplementedError("TODO")


def dispatch(event: str, *args: Any) -> Any:
    """Call the handler registered for `event` with `args`.
    If there is none, raise KeyError with a clear message.
    """
    raise NotImplementedError("TODO")
