"""Dataclasses.

Convertí cada clase en una dataclass con las opciones adecuadas y completá los métodos.
"""

import math  # noqa: F401
from dataclasses import asdict, dataclass, field, replace  # noqa: F401
from typing import Any


class Punto:
    """Punto 2D inmutable y hashable (usá `frozen=True`) con campos `x` e `y`.

    - `distancia(otro)`: distancia euclídea (pista: `math.hypot`).
    - `p + q`: suma componente a componente.
    """

    def distancia(self, otro: "Punto") -> float:
        raise NotImplementedError("TODO")


class Version:
    """Versión semántica comparable (`order=True`), inmutable.

    Campos: `mayor`, `menor=0`, `parche=0`.
    - `Version.desde_str("1.2.3")`: acepta también "1.2" y "1". Inválido → ValueError.
    - `str(Version(1, 2, 3)) == "1.2.3"` (el repr autogenerado se mantiene).
    """

    @classmethod
    def desde_str(cls, texto: str) -> "Version":
        raise NotImplementedError("TODO")


class Pedido:
    """Pedido mutable.

    Campos: `cliente: str`, `items: list[str]` (lista nueva por instancia, vacía por
    defecto) y `estado: str = "nuevo"`.

    - `__post_init__`: si `cliente` está vacío (o solo espacios) → ValueError.
    - `con_estado(nuevo)`: devuelve una COPIA con el estado cambiado (pista: `replace`).
    - `a_dict()`: el pedido como dict (pista: `asdict`).
    """

    def con_estado(self, nuevo: str) -> "Pedido":
        raise NotImplementedError("TODO")

    def a_dict(self) -> dict[str, Any]:
        raise NotImplementedError("TODO")
