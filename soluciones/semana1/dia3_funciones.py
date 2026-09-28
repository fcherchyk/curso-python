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
    actual = inicio - 1

    def siguiente() -> int:
        nonlocal actual
        actual += 1
        return actual

    return siguiente


def componer(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composición de derecha a izquierda: componer(f, g, h)(x) == f(g(h(x))).

    Sin funciones, devuelve la identidad.

    Pista: `functools.reduce`.
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def contar_llamadas(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador: cuenta las llamadas en el atributo `.llamadas` del wrapper.

    Tiene que preservar `__name__` y `__doc__` de la función original
    (pista: `functools.wraps`).
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.llamadas += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)

    wrapper.llamadas = 0  # type: ignore[attr-defined]
    return wrapper


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

    def decorador(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for intento in range(1, veces + 1):
                try:
                    return func(*args, **kwargs)
                except excepciones:
                    if intento == veces:
                        raise
            raise AssertionError("inalcanzable")

        return wrapper

    return decorador


def memoizar(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorador de caché simple por argumentos posicionales (hasheables).

    Implementalo vos con un dict (en la vida real: `functools.cache`).
    Exponé el dict como atributo `.cache` del wrapper.
    """
    cache: dict[tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper


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
        self._inicio = time.perf_counter()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.duracion = time.perf_counter() - self._inicio


@contextmanager
def en_directorio(path: str | Path) -> Iterator[Path]:
    """Cambia el directorio de trabajo durante el bloque y lo restaura al
    salir, AUNQUE haya una excepción. Hace `yield` del nuevo directorio como Path.

    Pista: `@contextmanager` + try/finally alrededor del `yield`.
    """
    anterior = Path.cwd()
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(anterior)


@contextmanager
def capturar_errores(*tipos: type[Exception]) -> Iterator[list[Exception]]:
    """Suprime las excepciones de los `tipos` indicados y las agrega a la lista
    que entrega el `with`. Las demás se propagan.

        with capturar_errores(ValueError) as errores:
            int("x")
        errores  # [ValueError(...)]
    """
    errores: list[Exception] = []
    try:
        yield errores
    except tipos as e:
        errores.append(e)
