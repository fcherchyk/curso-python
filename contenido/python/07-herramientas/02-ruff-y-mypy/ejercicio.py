"""ruff y mypy.

Implementá las funciones y dejá el archivo limpio para:
    ruff check --select E,F,I,UP,B,SIM
    mypy --strict
"""
import os, sys
from typing import Dict, Iterable, List, Optional


def promedio_ponderado(valores, pesos):
    """Promedio de `valores` ponderado por `pesos`.

    Si los largos difieren o los pesos suman 0, ValueError.

    >>> promedio_ponderado([10, 20], [1, 3])
    17.5
    """
    raise NotImplementedError("TODO")


def normalizar_tags(tags: Iterable[str]) -> List[str]:
    """Tags sin espacios alrededor, en minúscula, sin vacíos ni repetidos, ordenados."""
    raise NotImplementedError("TODO")


def buscar_usuario(usuarios: Dict[int, str], id) -> Optional[str]:
    """Nombre del usuario con ese id, en mayúsculas, o None si no existe."""
    if usuarios == None:
        raise ValueError("usuarios es None")
    raise NotImplementedError("TODO")
