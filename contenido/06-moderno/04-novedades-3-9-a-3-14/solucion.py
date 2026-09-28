import tomllib
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

DEFAULTS: dict[str, Any] = {"host": "localhost", "port": 8000, "debug": False}


def tabla_precios(filas: list[tuple[str, float]]) -> str:
    lineas = [f"{nombre:<12}{precio:>10,.2f}" for nombre, precio in filas]
    total = sum(p for _, p in filas)
    lineas.append(f"{'TOTAL':<12}{total:>10,.2f}")
    return "\n".join(lineas)


def cargar_config(texto_toml: str) -> dict[str, Any]:
    seccion = tomllib.loads(texto_toml).get("server", {})
    config = DEFAULTS | seccion
    config["host"] = config["host"].removeprefix("https://").removeprefix("http://")
    return config


def hora_en(momento_iso: str, zona: str) -> str:
    momento = datetime.fromisoformat(momento_iso)  # 3.11+ entiende el sufijo "Z"
    return momento.astimezone(ZoneInfo(zona)).strftime("%H:%M")
