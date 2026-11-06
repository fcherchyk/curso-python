"""Modern typing and generics.

Use the 3.12 syntax (`class Stack[T]`, `def f[T](...)`); the tests check it.
"""

from collections.abc import Callable, Iterable  # noqa: F401
from typing import TypedDict


class Stack:  # ← make it generic: class Stack[T]
    """Generic (LIFO) stack.

    - `push(x)`, `pop()` (empty → IndexError("empty stack")), `peek()` (or None)
    - `len(stack)`, and `bool(stack)` is False when it's empty
    - `repr(Stack([1, 2])) == "Stack([1, 2])"`
    """

    def __init__(self, items: Iterable[object] = ()) -> None:
        raise NotImplementedError("TODO")


def first(xs, default=None):  # ← type it with a generic T
    """First element of any iterable, or `default` if it's empty."""
    raise NotImplementedError("TODO")


def group_by(xs, key):  # ← type it with two generics T and K
    """Group the elements by `key(x)`, preserving order.

    Expected signature: `(xs: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]`.

    >>> group_by(["alice", "bob", "amy"], lambda s: s[0])
    {'a': ['alice', 'amy'], 'b': ['bob']}
    """
    raise NotImplementedError("TODO")


class UserJSON(TypedDict):
    id: int
    name: str
    active: bool


def active_names(users: list[UserJSON]) -> list[str]:
    """Names of the active users, sorted by id."""
    raise NotImplementedError("TODO")

