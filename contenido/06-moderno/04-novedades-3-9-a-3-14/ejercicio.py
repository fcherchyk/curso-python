"""Novedades de 3.9 a 3.14."""

import tomllib  # noqa: F401
from datetime import datetime  # noqa: F401
from typing import Any
from zoneinfo import ZoneInfo  # noqa: F401

DEFAULTS: dict[str, Any] = {"host": "localhost", "port": 8000, "debug": False}


def tabla_precios(filas: list[tuple[str, float]]) -> str:
    """Tabla de ancho fijo, una línea por fila, unidas con "\\n":

    - nombre alineado a la izquierda en 12 caracteres
    - precio alineado a la derecha en 10, con separador de miles y 2 decimales
    - al final una línea "TOTAL" con el mismo formato

    >>> print(tabla_precios([("café", 1500.5)]))
    café          1,500.50
    TOTAL         1,500.50
    """
    raise NotImplementedError("TODO")


def cargar_config(texto_toml: str) -> dict[str, Any]:
    """Parseá el TOML y devolvé la sección [server] fusionada sobre DEFAULTS
    (sin mutar DEFAULTS). Si no hay sección [server], una copia de DEFAULTS.

    Además, si "host" empieza con "http://" o "https://", quitá el prefijo.
    """
    raise NotImplementedError("TODO")


def hora_en(momento_iso: str, zona: str) -> str:
    """Convertí un momento ISO 8601 con zona (por ejemplo "2026-01-15T15:30:00Z") a la
    zona IANA indicada y devolvé la hora local como "HH:MM".

    >>> hora_en("2026-01-15T15:30:00Z", "America/Argentina/Buenos_Aires")
    '12:30'
    """
    raise NotImplementedError("TODO")
