"""Code under test (don't modify it: write the tests in exercise.py)."""

from collections.abc import Iterable
from pathlib import Path
from typing import Any, Protocol

BASE = "https://api.weather.test/v1"


class HttpClient(Protocol):
    def get_json(self, url: str) -> dict[str, Any]: ...


def temperature(city: str, client: HttpClient) -> float:
    """Current temperature of the city, rounded to 1 decimal."""
    data = client.get_json(f"{BASE}/current?city={city}")
    return round(data["temp_c"], 1)


def summary(cities: Iterable[str], client: HttpClient) -> dict[str, float]:
    """Temperature of each city. Those that fail with LookupError are skipped."""
    result = {}
    for city in cities:
        try:
            result[city] = temperature(city, client)
        except LookupError:
            continue
    return result


def save_report(path: Path, temperatures: dict[str, float]) -> None:
    """Writes "city: temp" per line, sorted by city."""
    lines = [f"{c}: {t}" for c, t in sorted(temperatures.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
