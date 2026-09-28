import math
from collections.abc import Iterator


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Vector):
            return NotImplemented
        return (self.x, self.y) == (otro.x, otro.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, otro: "Vector") -> "Vector":
        if not isinstance(otro, Vector):
            return NotImplemented
        return Vector(self.x + otro.x, self.y + otro.y)

    def __sub__(self, otro: "Vector") -> "Vector":
        if not isinstance(otro, Vector):
            return NotImplemented
        return Vector(self.x - otro.x, self.y - otro.y)

    def __mul__(self, k: float) -> "Vector":
        if not isinstance(k, (int, float)):
            return NotImplemented
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return bool(self.x or self.y)


class Item:
    def __init__(self, nombre: str, precio: float, cantidad: int = 1) -> None:
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad


class Carrito:
    def __init__(self) -> None:
        self._items: list[Item] = []

    def agregar(self, item: Item) -> "Carrito":
        self._items.append(item)
        return self

    @property
    def total(self) -> float:
        return round(sum(i.precio * i.cantidad for i in self._items), 2)

    def __len__(self) -> int:
        return sum(i.cantidad for i in self._items)

    def __iter__(self) -> Iterator[Item]:
        return iter(self._items)

    def __contains__(self, nombre: object) -> bool:
        return any(i.nombre == nombre for i in self._items)

    def __getitem__(self, i: int) -> Item:
        return self._items[i]
