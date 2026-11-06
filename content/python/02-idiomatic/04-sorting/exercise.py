"""Ordenar.

Usá `sorted`, `max` y `operator.itemgetter` con el parámetro `key`.
"""

from operator import itemgetter  # noqa: F401  (te va a servir)


def ordenar_personas(personas: list[dict[str, str | int]]) -> list[str]:
    """Devolvé los nombres ordenados por edad descendente y, a igual edad,
    por nombre ascendente.

    Cada persona es `{"nombre": str, "edad": int}`.

    >>> ordenar_personas([{"nombre": "Zoe", "edad": 30}, {"nombre": "Ana", "edad": 25},
    ...                   {"nombre": "Beto", "edad": 30}])
    ['Beto', 'Zoe', 'Ana']
    """
    raise NotImplementedError("TODO")


def mas_caro(productos: list[dict[str, str | float]]) -> str | None:
    """Nombre del producto con mayor `precio`, o None si la lista está vacía.

    Ante empates, el primero que aparece.

    >>> mas_caro([{"nombre": "pan", "precio": 1.2}, {"nombre": "café", "precio": 9.8}])
    'café'
    """
    raise NotImplementedError("TODO")


def ordenar_sin_mayusculas(palabras: list[str]) -> list[str]:
    """Ordená alfabéticamente sin distinguir mayúsculas de minúsculas.

    Las palabras se devuelven tal como vinieron (no las pases a minúscula).

    >>> ordenar_sin_mayusculas(["banana", "Ana", "Cereza"])
    ['Ana', 'banana', 'Cereza']
    """
    raise NotImplementedError("TODO")


def ordenar_por(filas: list[dict[str, str]], *campos: str) -> list[dict[str, str]]:
    """Ordená las filas por los campos indicados, en ese orden de prioridad.

    Sin campos, devolvé una copia sin cambiar el orden.

    >>> filas = [{"pais": "AR", "ciudad": "Rosario"}, {"pais": "AR", "ciudad": "Córdoba"}]
    >>> [f["ciudad"] for f in ordenar_por(filas, "pais", "ciudad")]
    ['Córdoba', 'Rosario']
    """
    raise NotImplementedError("TODO")
