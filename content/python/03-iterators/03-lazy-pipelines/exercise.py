"""Pipelines perezosos."""

import itertools  # noqa: F401
from collections.abc import Iterable, Iterator


def primeros_cuadrados_pares(numeros: Iterable[int], n: int) -> list[int]:
    """Los primeros `n` cuadrados pares de `numeros`.

    `numeros` puede ser INFINITO (ej. `itertools.count()`): armá un pipeline
    perezoso con generator expressions y cortalo con `islice`.

    >>> primeros_cuadrados_pares(range(1, 100), 3)
    [4, 16, 36]
    """
    raise NotImplementedError("TODO")


def en_lotes(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    """Partí en tuplas de tamaño `n` (la última puede ser más corta).

    Tiene que funcionar con listas y con iteradores infinitos (sin len ni slicing),
    y ser perezoso. Implementalo con `islice` (no uses `itertools.batched`).

    >>> list(en_lotes(range(5), 2))
    [(0, 1), (2, 3), (4,)]
    """
    raise NotImplementedError("TODO")


def parsear_accesos(lineas: Iterable[str]) -> Iterator[tuple[str, int, int]]:
    """Generador que parsea líneas de log con el formato `IP METODO RUTA STATUS BYTES`
    y produce tuplas (ip, status, bytes).

    Salteá las líneas mal formadas (cantidad de campos distinta de 5 o números inválidos).

    >>> list(parsear_accesos(["1.1.1.1 GET / 200 512", "basura"]))
    [('1.1.1.1', 200, 512)]
    """
    raise NotImplementedError("TODO")


def bytes_por_status(lineas: Iterable[str]) -> dict[int, int]:
    """Total de bytes por código de status, recorriendo las líneas UNA sola vez.

    Reutilizá `parsear_accesos` como etapa del pipeline. Devolvé las claves ordenadas.

    >>> bytes_por_status(["a GET / 200 10", "b GET / 500 5", "c GET / 200 1"])
    {200: 11, 500: 5}
    """
    raise NotImplementedError("TODO")
