import itertools
from collections import deque
from collections.abc import Iterable, Iterator


def ventanas(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    ventana: deque[int] = deque(maxlen=n)
    for x in iterable:
        ventana.append(x)
        if len(ventana) == n:
            yield tuple(ventana)


def comprimir_repetidos(texto: str) -> list[tuple[str, int]]:
    return [(c, sum(1 for _ in grupo)) for c, grupo in itertools.groupby(texto)]


def combinaciones_que_suman(nums: list[int], k: int, objetivo: int) -> list[tuple[int, ...]]:
    return [c for c in itertools.combinations(nums, k) if sum(c) == objetivo]


def saldos(inicial: float, movimientos: Iterable[float]) -> list[float]:
    return list(itertools.accumulate(movimientos, initial=inicial))
