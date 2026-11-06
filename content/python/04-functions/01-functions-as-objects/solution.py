import functools
import operator
from collections.abc import Callable
from typing import Any

OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
}


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def apply_n_times(func: Callable[[Any], Any], n: int, x: Any) -> Any:
    for _ in range(n):
        x = func(x)
    return x


def calculate(op: str, a: float, b: float) -> float:
    try:
        function = OPERATIONS[op]
    except KeyError:
        raise ValueError(f"unknown operation: {op!r}") from None
    return function(a, b)


def base_parser(base: int) -> Callable[[str], int]:
    return functools.partial(int, base=base)
