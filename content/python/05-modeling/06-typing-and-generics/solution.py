from collections.abc import Callable, Iterable
from typing import TypedDict


class Stack[T]:
    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items: list[T] = list(items)

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("empty stack")
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


def first[T](xs: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(xs), default)


def group_by[T, K](xs: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    groups: dict[K, list[T]] = {}
    for x in xs:
        groups.setdefault(key(x), []).append(x)
    return groups


class UserJSON(TypedDict):
    id: int
    name: str
    active: bool


def active_names(users: list[UserJSON]) -> list[str]:
    return [u["name"] for u in sorted(users, key=lambda u: u["id"]) if u["active"]]
