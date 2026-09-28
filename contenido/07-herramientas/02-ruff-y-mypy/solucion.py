"""ruff y mypy: versión limpia."""

from collections.abc import Iterable


def promedio_ponderado(valores: list[float], pesos: list[float]) -> float:
    if len(valores) != len(pesos):
        raise ValueError("valores y pesos tienen que tener el mismo largo")
    total_pesos = sum(pesos)
    if total_pesos == 0:
        raise ValueError("los pesos suman 0")
    return sum(v * p for v, p in zip(valores, pesos, strict=True)) / total_pesos


def normalizar_tags(tags: Iterable[str]) -> list[str]:
    return sorted({t.strip().lower() for t in tags if t.strip()})


def buscar_usuario(usuarios: dict[int, str], id: int) -> str | None:
    nombre = usuarios.get(id)
    return nombre.upper() if nombre is not None else None
