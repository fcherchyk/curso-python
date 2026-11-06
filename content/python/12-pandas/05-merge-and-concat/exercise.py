"""Combinar tablas: merge, join y concat."""

import pandas as pd


def enriquecer(ventas: pd.DataFrame, productos: pd.DataFrame) -> pd.DataFrame:
    """Agregá a cada venta la categoría y el precio_unitario del catálogo, SIN perder ventas
    (las de productos fuera del catálogo quedan con nulos). Validá que la relación sea
    muchos-a-uno (si el catálogo tiene productos repetidos, tiene que levantar MergeError).
    Agregá también "total" = cantidad * precio_unitario.
    """
    raise NotImplementedError("TODO")


def productos_fuera_de_catalogo(ventas: pd.DataFrame, productos: pd.DataFrame) -> list[str]:
    """Productos vendidos que no están en el catálogo, sin repetir y ordenados (indicator=True)."""
    raise NotImplementedError("TODO")


def facturacion_por_categoria(ventas: pd.DataFrame, productos: pd.DataFrame) -> dict[str, float]:
    """Suma de total por categoría, solo para ventas con producto en catálogo (inner)."""
    raise NotImplementedError("TODO")


def apilar(partes: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Concatená los DataFrames uno debajo del otro, con una columna "lote" (la clave del dict)
    como PRIMERA columna y un índice 0..n-1.
    """
    raise NotImplementedError("TODO")
