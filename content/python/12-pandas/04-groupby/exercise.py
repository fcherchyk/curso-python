"""groupby: agrupar y agregar.

`ventas` tiene índice "id" y las columnas fecha, sucursal, producto, cantidad, categoria,
precio_unitario y total (= cantidad * precio_unitario).
"""

import pandas as pd


def total_por_sucursal(ventas: pd.DataFrame) -> pd.Series:
    """Facturación (suma de total) por sucursal, de mayor a menor."""
    raise NotImplementedError("TODO")


def resumen_por_categoria(ventas: pd.DataFrame) -> pd.DataFrame:
    """Por categoría, con agregaciones con nombre:
    unidades (suma de cantidad), facturacion (suma de total), ticket_promedio (promedio de total,
    redondeado a 2) y productos (cantidad de productos distintos).
    Ordenado por facturacion descendente.
    """
    raise NotImplementedError("TODO")


def participacion_en_sucursal(ventas: pd.DataFrame) -> pd.Series:
    """Para cada venta, total / facturación de SU sucursal (transform). Mismo índice que ventas."""
    raise NotImplementedError("TODO")


def tabla_sucursal_categoria(ventas: pd.DataFrame) -> pd.DataFrame:
    """Tabla dinámica: filas = sucursal, columnas = categoría, celdas = suma de total, 0 si no hay."""
    raise NotImplementedError("TODO")


def producto_top_por_sucursal(ventas: pd.DataFrame) -> dict[str, str]:
    """Para cada sucursal, el producto con más UNIDADES vendidas."""
    raise NotImplementedError("TODO")
