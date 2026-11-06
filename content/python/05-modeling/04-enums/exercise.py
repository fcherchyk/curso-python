"""Enums."""

from enum import Enum, Flag, IntEnum, StrEnum, auto  # noqa: F401


class Status(Enum):  # ← change the base to StrEnum
    """Statuses of a task. The members have to be strings:
    `Status.PENDING == "pending"`.

    - `next()`: PENDING → IN_PROGRESS → DONE; from DONE, ValueError.
    - `is_final` (property): True only for DONE.
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    def next(self) -> "Status":
        raise NotImplementedError("TODO")


class Priority(Enum):  # ← change the base so they sort as integers
    LOW = 1
    MEDIUM = 2
    HIGH = 3


def most_urgent(tasks: list[tuple[str, Priority]]) -> list[str]:
    """Task names sorted from highest to lowest priority (stable on ties).

    >>> most_urgent([("a", Priority.LOW), ("b", Priority.HIGH)])
    ['b', 'a']
    """
    raise NotImplementedError("TODO")


class Permission(Enum):  # ← change the base to Flag
    """Combinable permissions: READ, WRITE, DELETE (with auto()) and ALL (all three)."""

    READ = 1


def can(permissions: Permission, required: Permission) -> bool:
    """Do `permissions` include EVERYTHING in `required`?

    >>> can(Permission.READ | Permission.WRITE, Permission.READ)
    True
    """
    raise NotImplementedError("TODO")
