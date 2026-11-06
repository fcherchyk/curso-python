from enum import Flag, IntEnum, StrEnum, auto


class Status(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    def next(self) -> "Status":
        members = list(Status)
        i = members.index(self)
        if i == len(members) - 1:
            raise ValueError("the task is already done")
        return members[i + 1]

    @property
    def is_final(self) -> bool:
        return self is Status.DONE


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


def most_urgent(tasks: list[tuple[str, Priority]]) -> list[str]:
    # sorted is stable: with reverse=True, ties keep their original order.
    return [name for name, _ in sorted(tasks, key=lambda t: t[1], reverse=True)]


class Permission(Flag):
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    ALL = READ | WRITE | DELETE


def can(permissions: Permission, required: Permission) -> bool:
    return required in permissions
