"""Graficar desde pandas. Cada función devuelve la figura (o el Axes, en estilizar)."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "ventas.csv"


def cargar() -> pd.DataFrame:
    """Lee ventas.csv con `fecha` como datetime y agrega `importe` = cantidad * precio_unitario."""
    ventas = pd.read_csv(CSV, parse_dates=["fecha"])
    return ventas.assign(importe=ventas["cantidad"] * ventas["precio_unitario"])


def estilizar(ax: Axes, titulo: str, xlabel: str, ylabel: str) -> Axes:
    """Pone título y etiquetas, oculta los bordes superior y derecho,
    y activa la grilla solo en el eje Y. Devuelve el mismo ax.
    """
    raise NotImplementedError("TODO")


def lineas_por_sucursal(ventas: pd.DataFrame) -> Figure:
    """Importe total por mes (index: período mensual) y sucursal (una columna cada una),
    con pivot_table, graficado con df.plot(ax=ax, marker="o").
    Estilizado con título "Importe mensual por sucursal", xlabel "Mes", ylabel "Importe ($)".
    """
    raise NotImplementedError("TODO")


def barras_por_categoria(ventas: pd.DataFrame) -> Figure:
    """Importe total por categoría, ordenado de menor a mayor, graficado con .plot.barh(ax=ax)
    (la mayor queda arriba). Estilizado con título "Importe por categoría",
    xlabel "Importe ($)", ylabel "" (vacío).
    """
    raise NotImplementedError("TODO")
