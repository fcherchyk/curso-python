"""Generadores.

Todas las funciones tienen que ser GENERADORES (usar `yield`), no devolver listas.
"""

from collections.abc import Iterable, Iterator


def fibonacci() -> Iterator[int]:
    """Generador infinito: 0, 1, 1, 2, 3, 5, ...

    Probalo con `itertools.islice(fibonacci(), 10)`.
    """
    raise NotImplementedError("TODO")


def lineas_utiles(lineas: Iterable[str]) -> Iterator[str]:
    """Generá las líneas sin espacios a los costados, salteando las vacías y los
    comentarios (las que empiezan con '#' después del strip).
    """
    raise NotImplementedError("TODO")


def aplanar_profundo(anidado: Iterable[object]) -> Iterator[object]:
    """Aplaná listas y tuplas anidadas a cualquier profundidad.

    Los strings NO se abren (son iterables, pero se tratan como átomos).

    Pista: recursión + `yield from`.

    >>> list(aplanar_profundo([1, [2, (3, [4])], "ab"]))
    [1, 2, 3, 4, 'ab']
    """
    raise NotImplementedError("TODO")


def rango_decimal(inicio: float, fin: float, paso: float) -> Iterator[float]:
    """Como `range` pero con floats: inicio, inicio+paso, ... mientras sea < fin.

    Para no acumular error de redondeo, calculá cada valor como `inicio + i * paso`
    y redondeá a 10 decimales. Si paso <= 0, levantá ValueError (¡al llamar a next!).

    >>> list(rango_decimal(0, 0.5, 0.1))
    [0.0, 0.1, 0.2, 0.3, 0.4]
    """
    raise NotImplementedError("TODO")
