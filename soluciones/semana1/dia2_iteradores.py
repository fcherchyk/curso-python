"""Día 2 — Iteradores, generadores e itertools.

    uv run pytest semana1/dia2_iteradores
"""

import itertools
from collections import deque
from collections.abc import Iterable, Iterator


class CuentaRegresiva:
    """Iterable que produce n, n-1, ..., 1.

    Tiene que poder recorrerse MÁS DE UNA VEZ: `__iter__` debe devolver un
    iterador nuevo cada vez. Lo más simple es que `__iter__` sea un generador.

    >>> list(CuentaRegresiva(3))
    [3, 2, 1]
    """

    def __init__(self, n: int) -> None:
        self.n = n

    def __iter__(self) -> Iterator[int]:
        yield from range(self.n, 0, -1)


class Contador:
    """Iterador "a mano" (sin generadores): produce inicio, inicio+1, ...,
    hasta `fin` exclusive.

    Implementá `__iter__` (devuelve self) y `__next__` (levanta StopIteration
    al terminar). Es un iterador: se consume una sola vez.
    """

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


def fibonacci() -> Iterator[int]:
    """Generador infinito: 0, 1, 1, 2, 3, 5, ...

    Probalo con `itertools.islice(fibonacci(), 10)`.
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def lineas_utiles(lineas: Iterable[str]) -> Iterator[str]:
    """Generá las líneas sin espacios al costado, salteando vacías y
    comentarios (las que empiezan con '#' después del strip).
    """
    for linea in lineas:
        linea = linea.strip()
        if linea and not linea.startswith("#"):
            yield linea


def aplanar_profundo(anidado: Iterable[object]) -> Iterator[object]:
    """Aplaná listas/tuplas anidadas a cualquier profundidad.

    Los strings NO se abren (son iterables, pero se tratan como átomos).

    Pista: recursión + `yield from`.

    >>> list(aplanar_profundo([1, [2, (3, [4])], "ab"]))
    [1, 2, 3, 4, 'ab']
    """
    for x in anidado:
        if isinstance(x, (list, tuple)):
            yield from aplanar_profundo(x)
        else:
            yield x


def en_lotes(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Partí en tuplas de tamaño `n` (la última puede ser más corta).

    Tiene que funcionar con iteradores (sin usar len ni slicing).
    Implementalo con `itertools.islice`; después mirá `itertools.batched` (3.12+).

    >>> list(en_lotes(range(5), 2))
    [(0, 1), (2, 3), (4,)]
    """
    it = iter(iterable)
    while lote := tuple(itertools.islice(it, n)):
        yield lote


def ventanas(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Ventanas deslizantes de tamaño `n`.

    Pista: `collections.deque(maxlen=n)`.

    >>> list(ventanas([1, 2, 3, 4], 3))
    [(1, 2, 3), (2, 3, 4)]
    """
    ventana: deque[int] = deque(maxlen=n)
    for x in iterable:
        ventana.append(x)
        if len(ventana) == n:
            yield tuple(ventana)


def comprimir_repetidos(texto: str) -> list[tuple[str, int]]:
    """Run-length encoding de caracteres consecutivos.

    Pista: `itertools.groupby`.

    >>> comprimir_repetidos("aaabcc")
    [('a', 3), ('b', 1), ('c', 2)]
    """
    return [(c, sum(1 for _ in grupo)) for c, grupo in itertools.groupby(texto)]


def combinaciones_que_suman(nums: list[int], k: int, objetivo: int) -> list[tuple[int, ...]]:
    """Todas las combinaciones de `k` elementos (en el orden de itertools)
    cuya suma es `objetivo`.

    Pista: `itertools.combinations`.
    """
    return [c for c in itertools.combinations(nums, k) if sum(c) == objetivo]


def primeros_cuadrados_pares(numeros: Iterable[int], n: int) -> list[int]:
    """Los primeros `n` cuadrados pares de `numeros`.

    `numeros` puede ser INFINITO (ej. `itertools.count()`): armá un pipeline
    perezoso con generator expressions y cortalo con `islice`.
    """
    cuadrados = (x * x for x in numeros)
    pares = (c for c in cuadrados if c % 2 == 0)
    return list(itertools.islice(pares, n))
