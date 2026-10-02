from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


class CuentaRegresiva:
    def __init__(self, n: int) -> None:
        self.n = n

    def __iter__(self) -> Iterator[int]:
        # Un generador nuevo en cada llamada: se puede recorrer muchas veces.
        yield from range(self.n, 0, -1)


class Contador:
    def __init__(self, inicio: int, fin: int) -> None:
        self.actual = inicio
        self.fin = fin

    def __iter__(self) -> "Contador":
        return self

    def __next__(self) -> int:
        if self.actual >= self.fin:
            raise StopIteration
        valor = self.actual
        self.actual += 1
        return valor


def primero(iterable: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(iterable), default)


def totales_y_porcentajes(montos: Iterable[float]) -> list[float]:
    montos = list(montos)  # materializamos: vamos a recorrer dos veces
    total = sum(montos)
    if total == 0:
        return [0.0] * len(montos)
    return [round(m * 100 / total, 1) for m in montos]
