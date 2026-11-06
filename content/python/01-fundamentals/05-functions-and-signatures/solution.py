def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items


def average(*numbers: float) -> float:
    if not numbers:
        raise ValueError("at least one number is required")
    return sum(numbers) / len(numbers)


def create_user(name: str, /, *, admin: bool = False, **extra: object) -> dict[str, object]:
    return {"name": name, "admin": admin, **extra}


def format_attributes(**attrs: object) -> str:
    parts = []
    for name, value in attrs.items():
        # `is True` / `is False`: 0 is a valid value, not a boolean.
        if value is None or value is False:
            continue
        parts.append(name if value is True else f'{name}="{value}"')
    return " ".join(parts)
