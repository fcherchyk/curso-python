"""ruff and mypy: clean version."""

from collections.abc import Iterable


def weighted_average(values: list[float], weights: list[float]) -> float:
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("the weights sum to 0")
    return sum(v * w for v, w in zip(values, weights, strict=True)) / total_weight


def normalize_tags(tags: Iterable[str]) -> list[str]:
    return sorted({t.strip().lower() for t in tags if t.strip()})


def find_user(users: dict[int, str], id: int) -> str | None:
    name = users.get(id)
    return name.upper() if name is not None else None
