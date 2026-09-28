"""Proyecto integrador: analizador de logs de acceso con CLI.

Implementá las piezas en orden (mirá la lección). Formato de cada línea:

    2026-09-20T10:15:32 GET /api/users 200 123ms
"""

import argparse  # noqa: F401
import re
import statistics  # noqa: F401
import sys  # noqa: F401
from collections import Counter  # noqa: F401
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path  # noqa: F401


class Metodo(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class LineaInvalida(ValueError):
    """La línea no respeta el formato esperado."""


@dataclass(frozen=True, slots=True)
class Registro:
    momento: datetime
    metodo: Metodo
    ruta: str
    status: int
    duracion_ms: int

    @property
    def es_error(self) -> bool:
        """True si el status es 5xx."""
        raise NotImplementedError("TODO")


PATRON = re.compile(
    r"^(?P<momento>\S+) (?P<metodo>[A-Z]+) (?P<ruta>/\S*) (?P<status>\d{3}) (?P<ms>\d+)ms$"
)


def parsear_linea(linea: str) -> Registro:
    """Convertí una línea en un Registro.

    Cualquier problema (regex que no matchea, fecha inválida, método
    desconocido) tiene que levantar `LineaInvalida` con la línea en el
    mensaje. Usá `raise ... from e` para encadenar la causa original.

    Pista: `PATRON.match(linea.strip())`, `datetime.fromisoformat`, `Metodo(...)`.
    """
    raise NotImplementedError("TODO")


def parsear(lineas: Iterable[str], invalidas: list[str] | None = None) -> Iterator[Registro]:
    """Generador de Registros. Saltea líneas vacías.

    Las líneas inválidas no cortan el procesamiento: se descartan y, si se
    pasó la lista `invalidas`, se agregan ahí (sin el salto de línea).
    """
    raise NotImplementedError("TODO")


@dataclass(frozen=True)
class Resumen:
    total: int
    errores: int
    por_status: dict[int, int]
    p50_ms: float
    p95_ms: float
    ruta_mas_lenta: str

    @property
    def tasa_error(self) -> float:
        """errores / total (0.0 si total es 0)."""
        raise NotImplementedError("TODO")


def resumir(registros: Iterable[Registro]) -> Resumen:
    """Calculá el resumen en UNA pasada sobre `registros` (puede ser un generador:
    materializalo en una lista una sola vez).

    - por_status: dict status -> cantidad, ordenado por status ascendente.
    - p50_ms / p95_ms: `statistics.quantiles(duraciones, n=100, method="inclusive")`,
      índices 49 y 94. Con menos de 2 registros, ambos valen la única duración (o 0.0).
    - ruta_mas_lenta: la ruta con MAYOR duración PROMEDIO ("" si no hay registros).
      Ante empate, la que apareció primero.
    """
    raise NotImplementedError("TODO")


def top_rutas(registros: Iterable[Registro], n: int = 5) -> list[tuple[str, int]]:
    """Las `n` rutas más pedidas con su cantidad (empates: orden de aparición)."""
    raise NotImplementedError("TODO")


def formatear(resumen: Resumen, top: list[tuple[str, int]], invalidas: int) -> str:
    """Texto del reporte. Formato exacto (ver test):

        Requests: 10 (inválidas: 1)
        Errores 5xx: 2 (20.0%)
        Latencia p50: 120.0 ms | p95: 900.0 ms
        Ruta más lenta: /api/report
        Status:
          200: 7
          500: 2
        Top rutas:
          /api/users      4
          /api/orders     3
    (ruta alineada a la izquierda en 15 caracteres, cantidad a la derecha en 4)
    """
    raise NotImplementedError("TODO")


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: `archivo` (posicional) y `--top N` (default 5).

    Imprime el reporte en stdout y devuelve 0. Si el archivo no existe,
    imprime "No existe: <archivo>" en stderr y devuelve 1.

    Pista: `argparse.ArgumentParser`, `type=Path`, `type=int`. Leé el archivo
    UNA vez a una lista de registros (vas a usarla dos veces).
    """
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    raise SystemExit(main())
