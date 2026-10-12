"""Figure y Axes. Usá la API orientada a objetos (fig, ax = plt.subplots()) y devolvé la figura."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
from matplotlib.figure import Figure


def grafico_ventas(meses: list[str], ventas: list[float]) -> Figure:
    """Línea con marcadores "o", figura de 8x4 pulgadas, título "Ventas mensuales",
    eje X "Mes", eje Y "Ventas ($)" y grilla activada.
    """
    raise NotImplementedError("TODO")


def comparar_sucursales(meses: list[str], series: dict[str, list[float]]) -> Figure:
    """Una línea por sucursal (clave del dict = label), en los MISMOS ejes, con leyenda
    y título "Ventas por sucursal".
    """
    raise NotImplementedError("TODO")


def guardar(fig: Figure, ruta: Path) -> Path:
    """Guardá la figura como PNG a 150 dpi con bbox_inches="tight", cerrala y devolvé la ruta."""
    raise NotImplementedError("TODO")
