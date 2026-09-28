"""Decoradores con parámetros."""

import functools  # noqa: F401
import warnings  # noqa: F401
from collections.abc import Callable
from typing import Any

Decorador = Callable[[Callable[..., Any]], Callable[..., Any]]


def repetir(n: int) -> Decorador:
    """La función decorada devuelve una lista con los resultados de llamarla `n` veces.

        @repetir(3)
        def f(): ...
        f()  # [r1, r2, r3]
    """
    raise NotImplementedError("TODO")


def reintentar(
    veces: int, excepciones: tuple[type[BaseException], ...] = (Exception,)
) -> Decorador:
    """Reintenta hasta `veces` intentos en total si la función levanta alguna de
    `excepciones`. Si se agotan, re-levanta la última. Otras excepciones se propagan
    de inmediato.
    """
    raise NotImplementedError("TODO")


def acotar(minimo: float, maximo: float) -> Decorador:
    """Acota el RESULTADO de la función al rango [minimo, maximo].

        @acotar(0, 100)
        def porcentaje(x): return x * 100
        porcentaje(1.5)  # 100
    """
    raise NotImplementedError("TODO")


def deprecado(func: Callable[..., Any] | None = None, *, reemplazo: str | None = None) -> Any:
    """Emite un `DeprecationWarning` cada vez que se llama a la función decorada.

    Funciona con y sin paréntesis:
        @deprecado                      -> "vieja está deprecada"
        @deprecado(reemplazo="nueva")   -> "vieja está deprecada; usá nueva"
    """
    raise NotImplementedError("TODO")
