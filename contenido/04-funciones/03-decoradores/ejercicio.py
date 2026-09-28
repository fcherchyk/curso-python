"""Decoradores."""

import functools  # noqa: F401
from collections.abc import Callable
from typing import Any


def contar_llamadas(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador: cuenta las llamadas en el atributo `.llamadas` del wrapper.

    Tiene que preservar `__name__` y `__doc__` de la función original y devolver
    su resultado.
    """
    raise NotImplementedError("TODO")


def memoizar(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador de caché por argumentos posicionales (hashables).

    Implementalo vos con un dict (en la vida real: `functools.cache`).
    Exponé el dict como atributo `.cache` del wrapper.
    """
    raise NotImplementedError("TODO")


MANEJADORES: dict[str, Callable[..., Any]] = {}


def manejador(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador de registro: guarda la función en MANEJADORES con su nombre como clave
    y la devuelve SIN envolver.
    """
    raise NotImplementedError("TODO")


def despachar(evento: str, *args: Any) -> Any:
    """Llamá al manejador registrado para `evento` con `args`.
    Si no hay ninguno, levantá KeyError con un mensaje claro.
    """
    raise NotImplementedError("TODO")
