"""Funciones como objetos."""

import functools  # noqa: F401
import operator  # noqa: F401
from collections.abc import Callable
from typing import Any


def componer(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composición de derecha a izquierda: componer(f, g, h)(x) == f(g(h(x))).

    Sin funciones, devuelve la identidad.

    >>> componer(str.title, str.strip)("  ana ")
    'Ana'
    """
    raise NotImplementedError("TODO")


def aplicar_n_veces(func: Callable[[Any], Any], n: int, x: Any) -> Any:
    """Aplicá `func` sobre `x` n veces seguidas: func(func(...func(x))).

    >>> aplicar_n_veces(lambda v: v * 2, 3, 1)
    8
    """
    raise NotImplementedError("TODO")


def calcular(op: str, a: float, b: float) -> float:
    """Calculadora con despacho por dict (nada de if/elif por operación).

    Soporta "+", "-", "*", "/" y "**". Con otra operación, ValueError.

    Pista: el módulo `operator`.

    >>> calcular("**", 2, 10)
    1024
    """
    raise NotImplementedError("TODO")


def parseador_de_base(base: int) -> Callable[[str], int]:
    """Devolvé una función que convierte strings a int en la `base` dada.

    Pista: `functools.partial`.

    >>> parseador_de_base(2)("1010")
    10
    """
    raise NotImplementedError("TODO")
