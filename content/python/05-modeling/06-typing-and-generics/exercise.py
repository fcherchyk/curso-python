"""Tipado moderno y genéricos.

Usá la sintaxis de 3.12 (`class Pila[T]`, `def f[T](...)`); los tests lo verifican.
"""

from collections.abc import Callable, Iterable  # noqa: F401
from typing import TypedDict


class Pila:  # ← hacela genérica: class Pila[T]
    """Pila (LIFO) genérica.

    - `apilar(x)`, `desapilar()` (vacía → IndexError("pila vacía")), `tope()` (o None)
    - `len(pila)`, y `bool(pila)` es False si está vacía
    - `repr(Pila([1, 2])) == "Pila([1, 2])"`
    """

    def __init__(self, items: Iterable[object] = ()) -> None:
        raise NotImplementedError("TODO")


def primero(xs, default=None):  # ← tipala con un genérico T
    """Primer elemento de cualquier iterable, o `default` si está vacío."""
    raise NotImplementedError("TODO")


def agrupar_por(xs, clave):  # ← tipala con dos genéricos T y K
    """Agrupá los elementos según `clave(x)`, respetando el orden.

    Firma esperada: `(xs: Iterable[T], clave: Callable[[T], K]) -> dict[K, list[T]]`.

    >>> agrupar_por(["ana", "beto", "abi"], lambda s: s[0])
    {'a': ['ana', 'abi'], 'b': ['beto']}
    """
    raise NotImplementedError("TODO")


class UsuarioJSON(TypedDict):
    id: int
    nombre: str
    activo: bool


def activos(usuarios: list[UsuarioJSON]) -> list[str]:
    """Nombres de los usuarios activos, ordenados por id."""
    raise NotImplementedError("TODO")

