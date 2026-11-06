"""Series y DataFrame."""

from pathlib import Path

import pandas as pd


def serie_precios(precios: dict[str, float]) -> pd.Series:
    """Series con los precios, nombre "precio" e índice ordenado alfabéticamente."""
    raise NotImplementedError("TODO")


def desde_registros(registros: list[dict[str, object]]) -> pd.DataFrame:
    """DataFrame con las columnas en el orden: producto, precio, stock."""
    raise NotImplementedError("TODO")


def cargar_ventas(ruta: Path | str) -> pd.DataFrame:
    """Leé ventas.csv con:
    - la columna "id" como índice
    - "fecha" como datetime
    - una columna nueva "total" = cantidad * precio_unitario
    """
    raise NotImplementedError("TODO")


def resumen(ventas: pd.DataFrame) -> dict[str, object]:
    """A partir de lo que devuelve cargar_ventas:
    {"filas": cantidad de ventas,
     "total": suma de "total",
     "ticket_promedio": promedio de "total" redondeado a 2 decimales,
     "venta_mayor": id (índice) de la venta con mayor total,
     "sucursal_mas_frecuente": la sucursal con más ventas (value_counts)}
    """
    raise NotImplementedError("TODO")
