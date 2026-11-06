import os
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


class Temporizador:
    def __init__(self) -> None:
        self.duracion: float | None = None
        self._inicio = 0.0

    def __enter__(self) -> "Temporizador":
        self._inicio = time.perf_counter()
        return self

    def __exit__(self, *exc_info: object) -> None:
        # Devolver None (falsy) deja que la excepción, si la hubo, siga su camino.
        self.duracion = time.perf_counter() - self._inicio


@contextmanager
def en_directorio(path: str | Path) -> Iterator[Path]:
    anterior = Path.cwd()
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(anterior)


@contextmanager
def capturar_errores(*tipos: type[Exception]) -> Iterator[list[Exception]]:
    errores: list[Exception] = []
    try:
        yield errores
    except tipos as e:
        errores.append(e)  # no re-levantamos: queda suprimida
