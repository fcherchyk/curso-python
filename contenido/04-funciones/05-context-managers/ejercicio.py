"""Context managers."""

import os  # noqa: F401
import time  # noqa: F401
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


class Temporizador:
    """Context manager que mide cuánto tarda el bloque.

        with Temporizador() as t:
            hacer_algo()
        print(t.duracion)   # segundos (float)

    Usá `time.perf_counter()`. `duracion` vale None hasta que termina el bloque
    (y se completa aunque el bloque falle). No suprime excepciones.
    """

    def __init__(self) -> None:
        self.duracion: float | None = None

    def __enter__(self) -> "Temporizador":
        raise NotImplementedError("TODO")

    def __exit__(self, *exc_info: object) -> None:
        raise NotImplementedError("TODO")


@contextmanager
def en_directorio(path: str | Path) -> Iterator[Path]:
    """Cambia el directorio de trabajo durante el bloque y lo restaura al salir,
    AUNQUE haya una excepción. Hace `yield` del nuevo directorio como Path.
    """
    raise NotImplementedError("TODO")
    yield  # (para que sea un generador; borrá esta línea al implementar)


@contextmanager
def capturar_errores(*tipos: type[Exception]) -> Iterator[list[Exception]]:
    """Suprime las excepciones de los `tipos` indicados y las agrega a la lista que
    entrega el `with`. Las demás se propagan.

        with capturar_errores(ValueError) as errores:
            int("x")
        errores  # [ValueError(...)]
    """
    raise NotImplementedError("TODO")
    yield  # (para que sea un generador; borrá esta línea al implementar)
