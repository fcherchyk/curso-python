"""Interfaces: Protocol vs. ABC."""

import math  # noqa: F401
from abc import ABC, abstractmethod  # noqa: F401
from collections.abc import Iterable
from typing import Protocol, runtime_checkable  # noqa: F401


class HasArea(Protocol):
    def area(self) -> float: ...


class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        raise NotImplementedError("TODO")


def total_area(shapes: Iterable[HasArea]) -> float:
    """Sum of the areas of anything with an `area()` method, without inheritance."""
    raise NotImplementedError("TODO")


class Notifier:  # ← turn it into an ABC with an abstract `send`
    """Abstract base for notifiers.

    - `send(recipient, message) -> bool`: ABSTRACT.
    - `send_to_all(recipients, message) -> int`: concrete; how many sends succeeded.
    """

    def send(self, recipient: str, message: str) -> bool:
        raise NotImplementedError("TODO")

    def send_to_all(self, recipients: Iterable[str], message: str) -> int:
        raise NotImplementedError("TODO")


class InMemoryNotifier(Notifier):
    """Implementation for tests: stores (recipient, message) in `self.sent`.
    Fails (returns False, without storing) if the recipient is empty.
    """

    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []


class Closeable(Protocol):  # ← make it checkable at runtime
    def close(self) -> None: ...


def close_all(objects: Iterable[object]) -> int:
    """Call `close()` on the objects that satisfy `Closeable` (ignore the rest) and
    return how many you closed.
    """
    raise NotImplementedError("TODO")
