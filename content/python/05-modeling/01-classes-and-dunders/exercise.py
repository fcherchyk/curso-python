"""Classes and the data model.

Implement the special methods (don't use dataclasses in this chapter).
"""

import math  # noqa: F401
from collections.abc import Iterator


class Vector:
    """Immutable 2D vector.

    - `repr(Vector(1, 2)) == "Vector(1, 2)"`
    - `==` by value; hashable (can be used in sets)
    - `v + w`, `v - w`, `v * k` and `k * v` (k a number)
    - `abs(v)` is the magnitude; `bool(v)` is False only for the zero vector
    - With unsupported types, the operators return NotImplemented
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        raise NotImplementedError("TODO")

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("TODO")

    def __hash__(self) -> int:
        raise NotImplementedError("TODO")

    def __add__(self, other: "Vector") -> "Vector":
        raise NotImplementedError("TODO")

    def __sub__(self, other: "Vector") -> "Vector":
        raise NotImplementedError("TODO")

    def __mul__(self, k: float) -> "Vector":
        raise NotImplementedError("TODO")

    # Also implement __rmul__, __abs__ and __bool__.


class Item:
    def __init__(self, name: str, price: float, quantity: int = 1) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity


class Cart:
    """Collection of Items.

    - `len(cart)`: number of UNITS (sum of `quantity`)
    - `for item in cart`: iterates over the items
    - `"bread" in cart`: there's some item with that name
    - `cart[0]`: the first item
    - `cart.total`: sum of price * quantity, rounded to 2 decimals
    - `add(item)` returns self for chaining
    """

    def __init__(self) -> None:
        self._items: list[Item] = []

    def add(self, item: Item) -> "Cart":
        raise NotImplementedError("TODO")

    @property
    def total(self) -> float:
        raise NotImplementedError("TODO")

    def __len__(self) -> int:
        raise NotImplementedError("TODO")

    def __iter__(self) -> Iterator[Item]:
        raise NotImplementedError("TODO")

    def __contains__(self, name: object) -> bool:
        raise NotImplementedError("TODO")

    def __getitem__(self, i: int) -> Item:
        raise NotImplementedError("TODO")
