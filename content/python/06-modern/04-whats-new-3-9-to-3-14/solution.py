import tomllib
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

DEFAULTS: dict[str, Any] = {"host": "localhost", "port": 8000, "debug": False}


def price_table(rows: list[tuple[str, float]]) -> str:
    lines = [f"{name:<12}{price:>10,.2f}" for name, price in rows]
    total = sum(p for _, p in rows)
    lines.append(f"{'TOTAL':<12}{total:>10,.2f}")
    return "\n".join(lines)


def load_config(toml_text: str) -> dict[str, Any]:
    section = tomllib.loads(toml_text).get("server", {})
    config = DEFAULTS | section
    config["host"] = config["host"].removeprefix("https://").removeprefix("http://")
    return config


def time_in(iso_moment: str, zone: str) -> str:
    moment = datetime.fromisoformat(iso_moment)  # 3.11+ understands the "Z" suffix
    return moment.astimezone(ZoneInfo(zone)).strftime("%H:%M")
