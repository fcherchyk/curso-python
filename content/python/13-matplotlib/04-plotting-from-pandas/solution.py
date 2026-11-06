from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "ventas.csv"


def cargar() -> pd.DataFrame:
    ventas = pd.read_csv(CSV, parse_dates=["fecha"])
    return ventas.assign(importe=ventas["cantidad"] * ventas["precio_unitario"])


def estilizar(ax: Axes, titulo: str, xlabel: str, ylabel: str) -> Axes:
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    return ax


def lineas_por_sucursal(ventas: pd.DataFrame) -> Figure:
    mensual = ventas.assign(mes=ventas["fecha"].dt.to_period("M")).pivot_table(
        index="mes", columns="sucursal", values="importe", aggfunc="sum"
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    mensual.plot(ax=ax, marker="o")
    estilizar(ax, "Importe mensual por sucursal", "Mes", "Importe ($)")
    return fig


def barras_por_categoria(ventas: pd.DataFrame) -> Figure:
    por_categoria = ventas.groupby("categoria")["importe"].sum().sort_values()
    fig, ax = plt.subplots()
    por_categoria.plot.barh(ax=ax)
    estilizar(ax, "Importe por categoría", "Importe ($)", "")
    return fig
