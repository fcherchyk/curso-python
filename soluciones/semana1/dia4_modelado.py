"""Día 4 — Modelado: dataclasses, enums, dunder methods, Protocols y genéricos.

    uv run pytest semana1/dia4_modelado
"""

import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Punto:
    """Punto 2D inmutable (y por lo tanto hasheable: se puede usar en sets)."""

    x: float
    y: float

    def distancia(self, otro: "Punto") -> float:
        """Distancia euclídea. Pista: `math.hypot`."""
        return math.hypot(self.x - otro.x, self.y - otro.y)

    def __add__(self, otro: "Punto") -> "Punto":
        """Suma componente a componente: `Punto(1, 2) + Punto(3, 4) == Punto(4, 6)`."""
        return Punto(self.x + otro.x, self.y + otro.y)


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
        partes = [int(p) for p in texto.split(".")]
        return cls(*partes)

    def __str__(self) -> str:
        """str(Version(1, 2, 3)) == "1.2.3" (el repr autogenerado queda igual)."""
        return f"{self.mayor}.{self.menor}.{self.parche}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Estado(StrEnum):
    """Estados de una tarea. StrEnum (3.11+): los miembros SON strings."""

    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    TERMINADO = "terminado"

    def siguiente(self) -> "Estado":
        """PENDIENTE -> EN_CURSO -> TERMINADO. Desde TERMINADO levanta ValueError.

        Pista: `list(Estado)` respeta el orden de definición.
        """
        miembros = list(Estado)
        i = miembros.index(self)
        if i == len(miembros) - 1:
            raise ValueError("la tarea ya está terminada")
        return miembros[i + 1]


# ---------------------------------------------------------------------------
# Composición + dunder methods
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Item:
    nombre: str
    precio: float
    cantidad: int = 1

    @property
    def subtotal(self) -> float:
        """precio * cantidad."""
        return self.precio * self.cantidad


@dataclass
class Carrito:
    """Carrito que se comporta como una colección de Items."""

    items: list[Item] = field(default_factory=list)  # ¡nunca `= []`!

    def agregar(self, item: Item) -> "Carrito":
        """Agrega el item y devuelve self (para encadenar llamadas)."""
        self.items.append(item)
        return self

    @property
    def total(self) -> float:
        """Suma de subtotales, redondeada a 2 decimales."""
        return round(sum(i.subtotal for i in self.items), 2)

    def __len__(self) -> int:
        """Cantidad de unidades (sumá `cantidad`, no la cantidad de Items)."""
        return sum(i.cantidad for i in self.items)

    def __iter__(self) -> Iterator[Item]:
        """Iterar un carrito recorre sus items."""
        return iter(self.items)

    def __contains__(self, nombre: object) -> bool:
        """`"pan" in carrito` es True si hay algún item con ese nombre."""
        return any(i.nombre == nombre for i in self.items)


# ---------------------------------------------------------------------------
# Protocols (duck typing estático)
# ---------------------------------------------------------------------------


class TieneArea(Protocol):
    def area(self) -> float: ...


@dataclass
class Circulo:
    radio: float

    def area(self) -> float:
        """pi * r^2."""
        return math.pi * self.radio**2


@dataclass
class Rectangulo:
    ancho: float
    alto: float

    def __post_init__(self) -> None:
        """Validá que ancho y alto no sean negativos (ValueError)."""
        if self.ancho < 0 or self.alto < 0:
            raise ValueError("dimensiones negativas")

    def area(self) -> float:
        """ancho * alto."""
        return self.ancho * self.alto


def area_total(figuras: Iterable[TieneArea]) -> float:
    """Suma de áreas de cualquier cosa con un método `area()`, sin herencia."""
    return sum(f.area() for f in figuras)


# ---------------------------------------------------------------------------
# Genéricos con la sintaxis de 3.12
# ---------------------------------------------------------------------------


class Pila[T]:
    """Pila (LIFO) genérica: `Pila[int]()`."""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items: list[T] = list(items)

    def apilar(self, item: T) -> None:
        """Pone un elemento arriba."""
        self._items.append(item)

    def desapilar(self) -> T:
        """Saca y devuelve el de arriba. Vacía -> IndexError("pila vacía")."""
        if not self._items:
            raise IndexError("pila vacía")
        return self._items.pop()

    def tope(self) -> T | None:
        """Devuelve el de arriba sin sacarlo, o None si está vacía."""
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        """Cantidad de elementos (y de paso hace que `if pila:` funcione)."""
        return len(self._items)

    def __repr__(self) -> str:
        """repr(Pila([1, 2])) == "Pila([1, 2])"."""
        return f"Pila({self._items!r})"


def primero[T](xs: Iterable[T], default: T | None = None) -> T | None:
    """Primer elemento de cualquier iterable, o `default` si está vacío.

    Pista: `next(iter(xs), default)`.
    """
    return next(iter(xs), default)
