"""Día 3 — Funciones de primera clase, closures, decoradores y context managers.

uv run pytest semana1/dia3_funciones
"""

import functools
import os
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


def crear_contador(inicio: int = 0) -> Callable[[], int]:
    """Devolvé una función que, cada vez que se llama, devuelve el siguiente
    entero empezando en `inicio`.

    Pista: closure + `nonlocal`.

    >>> c = crear_contador(5)
    >>> c(), c()
    (5, 6)
    """
    raise NotImplementedError("TODO")


def componer(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composición de derecha a izquierda: componer(f, g, h)(x) == f(g(h(x))).

    Sin funciones, devuelve la identidad.

    Pista: `functools.reduce`.
    """
    raise NotImplementedError("TODO")


def contar_llamadas(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador: cuenta las llamadas en el atributo `.llamadas` del wrapper.

    Tiene que preservar `__name__` y `__doc__` de la función original
    (pista: `functools.wraps`).
    """
    raise NotImplementedError("TODO")


def reintentar(
    veces: int, excepciones: tuple[type[BaseException], ...] = (Exception,)
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Fábrica de decoradores: reintenta la función hasta `veces` intentos en
    total si levanta alguna de `excepciones`. Si se agotan los intentos,
    re-levanta la última excepción. Otras excepciones se propagan de inmediato.

    Uso:
        @reintentar(3, excepciones=(ConnectionError,))
        def llamar_api(): ...

    Pista: tres niveles de funciones (fábrica -> decorador -> wrapper).
    """
    raise NotImplementedError("TODO")


def memoizar(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador de caché simple por argumentos posicionales (hasheables).

    Implementalo vos con un dict (en la vida real: `functools.cache`).
    Exponé el dict como atributo `.cache` del wrapper.
    """
    raise NotImplementedError("TODO")


class Temporizador:
    """Context manager que mide cuánto tarda el bloque.

        with Temporizador() as t:
            hacer_algo()
        print(t.duracion)   # segundos (float)

    Usá `time.perf_counter()`. `duracion` vale None hasta que termina el bloque.
    No suprime excepciones.
    """

    def __init__(self) -> None:
        self.duracion: float | None = None
        self._inicio = 0.0

    def __enter__(self) -> "Temporizador":
        raise NotImplementedError("TODO")

    def __exit__(self, *exc_info: object) -> None:
        raise NotImplementedError("TODO")


@contextmanager
def en_directorio(path: str | Path) -> Iterator[Path]:
    """Cambia el directorio de trabajo durante el bloque y lo restaura al
    salir, AUNQUE haya una excepción. Hace `yield` del nuevo directorio como Path.

    Pista: `@contextmanager` + try/finally alrededor del `yield`.
    """
    raise NotImplementedError("TODO")


@contextmanager
def capturar_errores(*tipos: type[Exception]) -> Iterator[list[Exception]]:
    """Suprime las excepciones de los `tipos` indicados y las agrega a la lista
    que entrega el `with`. Las demás se propagan.

        with capturar_errores(ValueError) as errores:
            int("x")
        errores  # [ValueError(...)]
    """
    raise NotImplementedError("TODO")
