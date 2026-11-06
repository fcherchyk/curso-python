"""Analizador de logs de acceso: solución de referencia."""

import argparse
import re
import statistics
import sys
from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path


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
        return 500 <= self.status < 600


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
    linea = linea.strip()
    if not (m := PATRON.match(linea)):
        raise LineaInvalida(linea)
    try:
        return Registro(
            momento=datetime.fromisoformat(m["momento"]),
            metodo=Metodo(m["metodo"]),
            ruta=m["ruta"],
            status=int(m["status"]),
            duracion_ms=int(m["ms"]),
        )
    except ValueError as e:
        raise LineaInvalida(linea) from e


def parsear(lineas: Iterable[str], invalidas: list[str] | None = None) -> Iterator[Registro]:
    """Generador de Registros. Saltea líneas vacías.

    Las líneas inválidas no cortan el procesamiento: se descartan y, si se
    pasó la lista `invalidas`, se agregan ahí (sin el salto de línea).
    """
    for linea in lineas:
        if not linea.strip():
            continue
        try:
            yield parsear_linea(linea)
        except LineaInvalida:
            if invalidas is not None:
                invalidas.append(linea.rstrip("\n"))


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
        return self.errores / self.total if self.total else 0.0


def resumir(registros: Iterable[Registro]) -> Resumen:
    """Calculá el resumen en UNA pasada sobre `registros` (puede ser un generador:
    materializalo en una lista una sola vez).

    - por_status: dict status -> cantidad, ordenado por status ascendente.
    - p50_ms / p95_ms: `statistics.quantiles(duraciones, n=100, method="inclusive")`,
      índices 49 y 94. Con menos de 2 registros, ambos valen la única duración (o 0.0).
    - ruta_mas_lenta: la ruta con MAYOR duración PROMEDIO ("" si no hay registros).
      Ante empate, la que apareció primero.
    """
    regs = list(registros)
    if not regs:
        return Resumen(0, 0, {}, 0.0, 0.0, "")
    duraciones = [r.duracion_ms for r in regs]
    if len(duraciones) >= 2:
        q = statistics.quantiles(duraciones, n=100, method="inclusive")
        p50, p95 = q[49], q[94]
    else:
        p50 = p95 = float(duraciones[0])
    por_ruta: dict[str, list[int]] = {}
    for r in regs:
        por_ruta.setdefault(r.ruta, []).append(r.duracion_ms)
    ruta_mas_lenta = max(por_ruta, key=lambda ruta: statistics.fmean(por_ruta[ruta]))
    return Resumen(
        total=len(regs),
        errores=sum(r.es_error for r in regs),
        por_status=dict(sorted(Counter(r.status for r in regs).items())),
        p50_ms=p50,
        p95_ms=p95,
        ruta_mas_lenta=ruta_mas_lenta,
    )


def top_rutas(registros: Iterable[Registro], n: int = 5) -> list[tuple[str, int]]:
    """Las `n` rutas más pedidas con su cantidad (empates: orden de aparición)."""
    return Counter(r.ruta for r in registros).most_common(n)


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
    lineas = [
        f"Requests: {resumen.total} (inválidas: {invalidas})",
        f"Errores 5xx: {resumen.errores} ({resumen.tasa_error:.1%})",
        f"Latencia p50: {resumen.p50_ms:.1f} ms | p95: {resumen.p95_ms:.1f} ms",
        f"Ruta más lenta: {resumen.ruta_mas_lenta}",
        "Status:",
        *(f"  {status}: {cant}" for status, cant in resumen.por_status.items()),
        "Top rutas:",
        *(f"  {ruta:<15}{cant:>4}" for ruta, cant in top),
    ]
    return "\n".join(lineas)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: `archivo` (posicional) y `--top N` (default 5).

    Imprime el reporte en stdout y devuelve 0. Si el archivo no existe,
    imprime "No existe: <archivo>" en stderr y devuelve 1.

    Pista: `argparse.ArgumentParser`, `type=Path`, `type=int`. Leé el archivo
    UNA vez a una lista de registros (vas a usarla dos veces).
    """
    parser = argparse.ArgumentParser(description="Analiza logs de acceso")
    parser.add_argument("archivo", type=Path)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)

    if not args.archivo.exists():
        print(f"No existe: {args.archivo}", file=sys.stderr)
        return 1

    invalidas: list[str] = []
    with args.archivo.open(encoding="utf-8") as f:
        registros = list(parsear(f, invalidas))
    print(formatear(resumir(registros), top_rutas(registros, args.top), len(invalidas)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
