"""Código a testear (no lo modifiques: escribí los tests en ejercicio.py)."""

from collections.abc import Iterable
from pathlib import Path
from typing import Any, Protocol

BASE = "https://api.clima.test/v1"


class ClienteHTTP(Protocol):
    def get_json(self, url: str) -> dict[str, Any]: ...


def temperatura(ciudad: str, cliente: ClienteHTTP) -> float:
    """Temperatura actual de la ciudad, redondeada a 1 decimal."""
    datos = cliente.get_json(f"{BASE}/actual?ciudad={ciudad}")
    return round(datos["temp_c"], 1)


def resumen(ciudades: Iterable[str], cliente: ClienteHTTP) -> dict[str, float]:
    """Temperatura de cada ciudad. Las que fallan con LookupError se omiten."""
    resultado = {}
    for ciudad in ciudades:
        try:
            resultado[ciudad] = temperatura(ciudad, cliente)
        except LookupError:
            continue
    return resultado


def guardar_reporte(ruta: Path, temperaturas: dict[str, float]) -> None:
    """Escribe "ciudad: temp" por línea, ordenado por ciudad."""
    lineas = [f"{c}: {t}" for c, t in sorted(temperaturas.items())]
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
