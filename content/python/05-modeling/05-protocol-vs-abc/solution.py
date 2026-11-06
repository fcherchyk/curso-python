import math
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Protocol, runtime_checkable


class HasArea(Protocol):
    def area(self) -> float: ...


class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius**2


def total_area(shapes: Iterable[HasArea]) -> float:
    return sum(s.area() for s in shapes)


class Notifier(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool: ...

    def send_to_all(self, recipients: Iterable[str], message: str) -> int:
        return sum(self.send(r, message) for r in recipients)


class InMemoryNotifier(Notifier):
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, recipient: str, message: str) -> bool:
        if not recipient:
            return False
        self.sent.append((recipient, message))
        return True


@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


def close_all(objects: Iterable[object]) -> int:
    closed = 0
    for obj in objects:
        if isinstance(obj, Closeable):
            obj.close()
            closed += 1
    return closed
