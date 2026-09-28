"""Día 4 — Modelado: dataclasses, enums, dunder methods, Protocols y genéricos.

uv run pytest semana1/dia4_modelado
"""

import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Punto:
    """Punto 2D inmutable (y por lo tanto hasheable: se puede usar en sets)."""

    x: float
    y: float

    def distancia(self, otro: "Punto") -> float:
        """Distancia euclídea. Pista: `math.hypot`."""
        raise NotImplementedError("TODO")

    def __add__(self, otro: "Punto") -> "Punto":
        """Suma componente a componente: `Punto(1, 2) + Punto(3, 4) == Punto(4, 6)`."""
        raise NotImplementedError("TODO")


@dataclass(frozen=True, order=True)
class Version:
    """Versión semántica comparable: `order=True` genera <, <=, >, >= comparando
    los campos en orden como si fueran una tupla.
    """

    mayor: int
    menor: int = 0
    parche: int = 0

    @classmethod
    def desde_str(cls, texto: str) -> "Version":
        """Constructor alternativo: "1.2.3" -> Version(1, 2, 3).

        Aceptá también "1.2" y "1". Un texto inválido levanta ValueError
        (`int()` ya lo hace por vos).
        """
        raise NotImplementedError("TODO")

    def __str__(self) -> str:
        """str(Version(1, 2, 3)) == "1.2.3" (el repr autogenerado queda igual)."""
        raise NotImplementedError("TODO")


class Estado(StrEnum):
    """Estados de una tarea. StrEnum (3.11+): los miembros SON strings."""

    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    TERMINADO = "terminado"

    def siguiente(self) -> "Estado":
        """PENDIENTE -> EN_CURSO -> TERMINADO. Desde TERMINADO levanta ValueError.

        Pista: `list(Estado)` respeta el orden de definición.
        """
        raise NotImplementedError("TODO")


@dataclass(frozen=True)
class Item:
    nombre: str
    precio: float
    cantidad: int = 1

    @property
    def subtotal(self) -> float:
        """precio * cantidad."""
        raise NotImplementedError("TODO")


@dataclass
class Carrito:
    """Carrito que se comporta como una colección de Items."""

    items: list[Item] = field(default_factory=list)

    def agregar(self, item: Item) -> "Carrito":
        """Agrega el item y devuelve self (para encadenar llamadas)."""
        raise NotImplementedError("TODO")

    @property
    def total(self) -> float:
        """Suma de subtotales, redondeada a 2 decimales."""
        raise NotImplementedError("TODO")

    def __len__(self) -> int:
        """Cantidad de unidades (sumá `cantidad`, no la cantidad de Items)."""
        raise NotImplementedError("TODO")

    def __iter__(self) -> Iterator[Item]:
        """Iterar un carrito recorre sus items."""
        raise NotImplementedError("TODO")

    def __contains__(self, nombre: object) -> bool:
        """`"pan" in carrito` es True si hay algún item con ese nombre."""
        raise NotImplementedError("TODO")


class TieneArea(Protocol):
    def area(self) -> float:
        raise NotImplementedError("TODO")


@dataclass
class Circulo:
    radio: float

    def area(self) -> float:
        """pi * r^2."""
        raise NotImplementedError("TODO")


@dataclass
class Rectangulo:
    ancho: float
    alto: float

    def __post_init__(self) -> None:
        """Validá que ancho y alto no sean negativos (ValueError)."""
        raise NotImplementedError("TODO")

    def area(self) -> float:
        """ancho * alto."""
        raise NotImplementedError("TODO")


def area_total(figuras: Iterable[TieneArea]) -> float:
    """Suma de áreas de cualquier cosa con un método `area()`, sin herencia."""
    raise NotImplementedError("TODO")


class Pila[T]:
    """Pila (LIFO) genérica: `Pila[int]()`."""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items: list[T] = list(items)

    def apilar(self, item: T) -> None:
        """Pone un elemento arriba."""
        raise NotImplementedError("TODO")

    def desapilar(self) -> T:
        """Saca y devuelve el de arriba. Vacía -> IndexError("pila vacía")."""
        raise NotImplementedError("TODO")

    def tope(self) -> T | None:
        """Devuelve el de arriba sin sacarlo, o None si está vacía."""
        raise NotImplementedError("TODO")

    def __len__(self) -> int:
        """Cantidad de elementos (y de paso hace que `if pila:` funcione)."""
        raise NotImplementedError("TODO")

    def __repr__(self) -> str:
        """repr(Pila([1, 2])) == "Pila([1, 2])"."""
        raise NotImplementedError("TODO")


def primero[T](xs: Iterable[T], default: T | None = None) -> T | None:
    """Primer elemento de cualquier iterable, o `default` si está vacío.

    Pista: `next(iter(xs), default)`.
    """
    raise NotImplementedError("TODO")
