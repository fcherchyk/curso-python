"""Seleccionar y filtrar.

`ventas` es el DataFrame de ventas.csv con índice "id", "fecha" parseada y la columna
"total" = cantidad * precio_unitario (como en el capítulo anterior; los tests lo arman).
"""

import pandas as pd


def ventas_grandes_de(ventas: pd.DataFrame, sucursal: str, minimo: float) -> pd.DataFrame:
    """Ventas de esa sucursal con total >= minimo, solo las columnas producto y total,
    ordenadas por total descendente.
    """
    raise NotImplementedError("TODO")


def de_productos(ventas: pd.DataFrame, productos: list[str]) -> pd.Series:
    """Cantidades (columna "cantidad") de las ventas de esos productos (isin)."""
    raise NotImplementedError("TODO")


def consulta(ventas: pd.DataFrame, categoria: str, minima_cantidad: int) -> list[int]:
    """Ids de las ventas de esa categoría con cantidad >= minima_cantidad, usando df.query
    con variables (@). Ordenados.
    """
    raise NotImplementedError("TODO")


def top_y_primera_etiqueta(ventas: pd.DataFrame) -> tuple[int, int]:
    """Ordená por total descendente y devolvé (id de la PRIMERA fila del orden, cantidad de
    la venta cuyo id es el MÁS CHICO). Usá iloc y loc respectivamente.
    """
    raise NotImplementedError("TODO")


def con_descuento(ventas: pd.DataFrame, categoria: str, pct: float) -> pd.DataFrame:
    """DataFrame NUEVO con precio_unitario y total reducidos un `pct` (0.1 = 10 %) en las
    ventas de esa categoría. NO modifiques `ventas`.
    """
    raise NotImplementedError("TODO")
