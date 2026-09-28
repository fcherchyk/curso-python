"""El protocolo de iteración."""

from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


class CuentaRegresiva:
    """Iterable que produce n, n-1, ..., 1.

    Tiene que poder recorrerse MÁS DE UNA VEZ: `__iter__` tiene que devolver un
    iterador nuevo cada vez.

    >>> list(CuentaRegresiva(3))
    [3, 2, 1]
    """

    def __init__(self, n: int) -> None:
        self.n = n

    def __iter__(self) -> Iterator[int]:
        raise NotImplementedError("TODO")


class Contador:
    """Iterador "a mano" (sin generadores): produce inicio, inicio+1, ...
    hasta `fin` (exclusive). Se consume una sola vez.

    Implementá `__iter__` (devuelve self) y `__next__` (levanta StopIteration al terminar).
    """

    def __init__(self, inicio: int, fin: int) -> None:
        raise NotImplementedError("TODO")

    def __iter__(self) -> "Contador":
        raise NotImplementedError("TODO")

    def __next__(self) -> int:
        raise NotImplementedError("TODO")


def primero(iterable: Iterable[T], default: T | None = None) -> T | None:
    """Primer elemento de cualquier iterable (incluso infinito), o `default` si está vacío.

    Pista: `next(iter(...), default)`.

    >>> primero(x for x in range(10) if x > 3)
    4
    """
    raise NotImplementedError("TODO")


def totales_y_porcentajes(montos: Iterable[float]) -> list[float]:
    """Porcentaje que representa cada monto sobre el total (redondeado a 1 decimal).

    ¡Ojo! `montos` puede ser un generador y necesitás recorrerlo dos veces.
    Si el total es 0, devolvé una lista de ceros.

    >>> totales_y_porcentajes([1, 1, 2])
    [25.0, 25.0, 50.0]
    """
    raise NotImplementedError("TODO")
