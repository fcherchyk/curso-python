from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def grafico_ventas(meses: list[str], ventas: list[float]) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(meses, ventas, marker="o")
    ax.set(title="Ventas mensuales", xlabel="Mes", ylabel="Ventas ($)")
    ax.grid(True, alpha=0.3)
    return fig


def comparar_sucursales(meses: list[str], series: dict[str, list[float]]) -> Figure:
    fig, ax = plt.subplots()
    for nombre, valores in series.items():
        ax.plot(meses, valores, label=nombre)
    ax.set_title("Ventas por sucursal")
    ax.legend()
    return fig


def guardar(fig: Figure, ruta: Path) -> Path:
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return ruta
