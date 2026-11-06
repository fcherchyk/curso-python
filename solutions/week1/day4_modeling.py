"""Day 4 — Modeling: dataclasses, enums, dunder methods, Protocols and generics.

    uv run pytest week1/day4_modeling
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
class Point:
    """Immutable 2D point (and therefore hashable: it can be used in sets)."""

    x: float
    y: float

    def distance(self, other: "Point") -> float:
        """Euclidean distance. Hint: `math.hypot`."""
        return math.hypot(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Point") -> "Point":
        """Component-wise addition: `Point(1, 2) + Point(3, 4) == Point(4, 6)`."""
        return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True, order=True)
class Version:
    """Comparable semantic version: `order=True` generates <, <=, >, >= by comparing
    the fields in order as if they were a tuple.
    """

    major: int
    minor: int = 0
    patch: int = 0

    @classmethod
    def from_str(cls, text: str) -> "Version":
        """Alternative constructor: "1.2.3" -> Version(1, 2, 3).

        Also accept "1.2" and "1". Invalid text raises ValueError
        (`int()` already does that for you).
        """
        parts = [int(p) for p in text.split(".")]
        return cls(*parts)

    def __str__(self) -> str:
        """str(Version(1, 2, 3)) == "1.2.3" (the auto-generated repr stays the same)."""
        return f"{self.major}.{self.minor}.{self.patch}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Status(StrEnum):
    """Task statuses. StrEnum (3.11+): the members ARE strings."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    def next_status(self) -> "Status":
        """PENDING -> IN_PROGRESS -> DONE. From DONE it raises ValueError.

        Hint: `list(Status)` keeps the definition order.
        """
        members = list(Status)
        i = members.index(self)
        if i == len(members) - 1:
            raise ValueError("the task is already done")
        return members[i + 1]


# ---------------------------------------------------------------------------
# Composition + dunder methods
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Item:
    name: str
    price: float
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        """price * quantity."""
        return self.price * self.quantity


@dataclass
class Cart:
    """Cart that behaves like a collection of Items."""

    items: list[Item] = field(default_factory=list)  # never `= []`!

    def add(self, item: Item) -> "Cart":
        """Add the item and return self (so calls can be chained)."""
        self.items.append(item)
        return self

    @property
    def total(self) -> float:
        """Sum of the subtotals, rounded to 2 decimal places."""
        return round(sum(i.subtotal for i in self.items), 2)

    def __len__(self) -> int:
        """Number of units (add up `quantity`, not the number of Items)."""
        return sum(i.quantity for i in self.items)

    def __iter__(self) -> Iterator[Item]:
        """Iterating over a cart walks its items."""
        return iter(self.items)

    def __contains__(self, name: object) -> bool:
        """`"bread" in cart` is True if there is an item with that name."""
        return any(i.name == name for i in self.items)


# ---------------------------------------------------------------------------
# Protocols (static duck typing)
# ---------------------------------------------------------------------------


class HasArea(Protocol):
    def area(self) -> float: ...


@dataclass
class Circle:
    radius: float

    def area(self) -> float:
        """pi * r^2."""
        return math.pi * self.radius**2


@dataclass
class Rectangle:
    width: float
    height: float

    def __post_init__(self) -> None:
        """Validate that width and height are not negative (ValueError)."""
        if self.width < 0 or self.height < 0:
            raise ValueError("negative dimensions")

    def area(self) -> float:
        """width * height."""
        return self.width * self.height


def total_area(shapes: Iterable[HasArea]) -> float:
    """Sum of the areas of anything with an `area()` method, without inheritance."""
    return sum(s.area() for s in shapes)


# ---------------------------------------------------------------------------
# Generics with the 3.12 syntax
# ---------------------------------------------------------------------------


class Stack[T]:
    """Generic stack (LIFO): `Stack[int]()`."""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items: list[T] = list(items)

    def push(self, item: T) -> None:
        """Put an element on top."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top element. Empty -> IndexError("empty stack")."""
        if not self._items:
            raise IndexError("empty stack")
        return self._items.pop()

    def peek(self) -> T | None:
        """Return the top element without removing it, or None if empty."""
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        """Number of elements (which also makes `if stack:` work)."""
        return len(self._items)

    def __repr__(self) -> str:
        """repr(Stack([1, 2])) == "Stack([1, 2])"."""
        return f"Stack({self._items!r})"


def first[T](xs: Iterable[T], default: T | None = None) -> T | None:
    """First element of any iterable, or `default` if it is empty.

    Hint: `next(iter(xs), default)`.
    """
    return next(iter(xs), default)
