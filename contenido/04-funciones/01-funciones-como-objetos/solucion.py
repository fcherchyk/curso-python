import functools
import operator
from collections.abc import Callable
from typing import Any

OPERACIONES: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
}


def componer(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def aplicar_n_veces(func: Callable[[Any], Any], n: int, x: Any) -> Any:
    for _ in range(n):
        x = func(x)
    return x


def calcular(op: str, a: float, b: float) -> float:
    try:
        funcion = OPERACIONES[op]
    except KeyError:
        raise ValueError(f"operación desconocida: {op!r}") from None
    return funcion(a, b)


def parseador_de_base(base: int) -> Callable[[str], int]:
    return functools.partial(int, base=base)
