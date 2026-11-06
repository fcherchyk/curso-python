"""Functions as objects."""

import functools  # noqa: F401
import operator  # noqa: F401
from collections.abc import Callable
from typing import Any


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Right-to-left composition: compose(f, g, h)(x) == f(g(h(x))).

    With no functions, return the identity.

    >>> compose(str.title, str.strip)("  alice ")
    'Alice'
    """
    raise NotImplementedError("TODO")


def apply_n_times(func: Callable[[Any], Any], n: int, x: Any) -> Any:
    """Apply `func` to `x` n times in a row: func(func(...func(x))).

    >>> apply_n_times(lambda v: v * 2, 3, 1)
    8
    """
    raise NotImplementedError("TODO")


def calculate(op: str, a: float, b: float) -> float:
    """Calculator with dict dispatch (no if/elif per operation).

    Supports "+", "-", "*", "/" and "**". Any other operation raises ValueError.

    Hint: the `operator` module.

    >>> calculate("**", 2, 10)
    1024
    """
    raise NotImplementedError("TODO")


def base_parser(base: int) -> Callable[[str], int]:
    """Return a function that converts strings to int in the given `base`.

    Hint: `functools.partial`.

    >>> base_parser(2)("1010")
    10
    """
    raise NotImplementedError("TODO")
