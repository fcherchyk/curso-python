from collections.abc import Callable
from typing import Any


def validate_user(data: dict[str, Any]) -> None:
    errors: list[Exception] = []
    name = data.get("name")
    if not isinstance(name, str) or not name:
        errors.append(ValueError("name"))
    age = data.get("age")
    if not isinstance(age, int):
        errors.append(TypeError("age"))
    elif age < 0:
        errors.append(ValueError("age"))
    if "@" not in str(data.get("email", "")):
        errors.append(ValueError("email"))
    if errors:
        raise ExceptionGroup("invalid user", errors)


def classify_errors(data: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"value": [], "type": []}
    try:
        validate_user(data)
    except* ValueError as group:
        result["value"] = [str(e) for e in group.exceptions]
    except* TypeError as group:
        result["type"] = [str(e) for e in group.exceptions]
    return result


def run_all(tasks: list[Callable[[], Any]]) -> list[Any]:
    results: list[Any] = []
    errors: list[Exception] = []
    for i, task in enumerate(tasks):
        try:
            results.append(task())
        except Exception as e:
            e.add_note(f"task {i}")
            errors.append(e)
    if errors:
        raise ExceptionGroup("tasks failed", errors)
    return results
