"""Clases y el modelo de datos.

Implementá los métodos especiales (no uses dataclasses en este capítulo).
"""

import math  # noqa: F401
from collections.abc import Iterator


class Vector:
    """Vector 2D inmutable.

    - `repr(Vector(1, 2)) == "Vector(1, 2)"`
    - `==` por valor; hashable (se puede usar en sets)
    - `v + w`, `v - w`, `v * k` y `k * v` (k número)
    - `abs(v)` es el módulo; `bool(v)` es False solo para el vector nulo
    - Con tipos no soportados, los operadores devuelven NotImplemented
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        raise NotImplementedError("TODO")

    def __eq__(self, otro: object) -> bool:
        raise NotImplementedError("TODO")

    def __hash__(self) -> int:
        raise NotImplementedError("TODO")

    def __add__(self, otro: "Vector") -> "Vector":
        raise NotImplementedError("TODO")

    def __sub__(self, otro: "Vector") -> "Vector":
        raise NotImplementedError("TODO")

    def __mul__(self, k: float) -> "Vector":
        raise NotImplementedError("TODO")

    # Completá también __rmul__, __abs__ y __bool__.


class Item:
    def __init__(self, nombre: str, precio: float, cantidad: int = 1) -> None:
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad


class Carrito:
    """Colección de Items.

    - `len(carrito)`: cantidad de UNIDADES (suma de `cantidad`)
    - `for item in carrito`: recorre los items
    - `"pan" in carrito`: hay algún item con ese nombre
    - `carrito[0]`: el primer item
    - `carrito.total`: suma de precio * cantidad, redondeada a 2 decimales
    - `agregar(item)` devuelve self para encadenar
    """

    def __init__(self) -> None:
        self._items: list[Item] = []

    def agregar(self, item: Item) -> "Carrito":
        raise NotImplementedError("TODO")

    @property
    def total(self) -> float:
        raise NotImplementedError("TODO")

    def __len__(self) -> int:
        raise NotImplementedError("TODO")

    def __iter__(self) -> Iterator[Item]:
        raise NotImplementedError("TODO")

    def __contains__(self, nombre: object) -> bool:
        raise NotImplementedError("TODO")

    def __getitem__(self, i: int) -> Item:
        raise NotImplementedError("TODO")
