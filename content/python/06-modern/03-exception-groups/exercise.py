"""ExceptionGroup, except* and notes."""

from collections.abc import Callable
from typing import Any


def validate_user(data: dict[str, Any]) -> None:
    """Validate ALL the fields and report every error together.

    - "name": non-empty str     -> otherwise ValueError("name")
    - "age": int                -> if it's not an int, TypeError("age")
    - "age" >= 0                -> if it's negative, ValueError("age")
    - "email": contains "@"     -> otherwise ValueError("email")

    If there are errors, raise `ExceptionGroup("invalid user", errors)`.
    Missing fields count as invalid.
    """
    raise NotImplementedError("TODO")


def classify_errors(data: dict[str, Any]) -> dict[str, list[str]]:
    """Call `validate_user` and classify the errors with `except*`.

    Return {"value": [...ValueError messages], "type": [...TypeError messages]}.
    If there are no errors, both lists stay empty.
    """
    raise NotImplementedError("TODO")


def run_all(tasks: list[Callable[[], Any]]) -> list[Any]:
    """Run every task (even if some fail) and return their results in order.

    If any of them raised an exception (Exception), at the end raise
    `ExceptionGroup("tasks failed", [...])` with those exceptions, each one with the
    note "task N" (N starting at 0).
    """
    raise NotImplementedError("TODO")
