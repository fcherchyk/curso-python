"""itertools: las piezas de lego."""

import itertools  # noqa: F401
from collections import deque  # noqa: F401
from collections.abc import Iterable, Iterator


def ventanas(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Ventanas deslizantes de tamaño `n`. Tiene que ser perezoso.

    Pista: `collections.deque(maxlen=n)`.

    >>> list(ventanas([1, 2, 3, 4], 3))
    [(1, 2, 3), (2, 3, 4)]
    """
    raise NotImplementedError("TODO")


def comprimir_repetidos(texto: str) -> list[tuple[str, int]]:
    """Run-length encoding de caracteres consecutivos.

    Pista: `itertools.groupby`.

    >>> comprimir_repetidos("aaabccaa")
    [('a', 3), ('b', 1), ('c', 2), ('a', 2)]
    """
    raise NotImplementedError("TODO")


def combinaciones_que_suman(nums: list[int], k: int, objetivo: int) -> list[tuple[int, ...]]:
    """Todas las combinaciones de `k` elementos (en el orden de itertools) cuya suma
    es `objetivo`.

    >>> combinaciones_que_suman([1, 2, 3, 4, 5], 2, 6)
    [(1, 5), (2, 4)]
    """
    raise NotImplementedError("TODO")


def saldos(inicial: float, movimientos: Iterable[float]) -> list[float]:
    """Saldo después de cada movimiento, empezando por el inicial.

    Pista: `itertools.accumulate(..., initial=...)`.

    >>> saldos(1000, [100, -30, 50])
    [1000, 1100, 1070, 1120]
    """
    raise NotImplementedError("TODO")
