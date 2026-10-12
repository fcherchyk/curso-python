"""Subplots, escalas y anotaciones. Cada función devuelve la figura."""

import matplotlib.pyplot as plt  # noqa: F401
from matplotlib.figure import Figure


def paneles(meses: list[str], series: dict[str, list[float]]) -> Figure:
    """Un panel por serie, en UNA fila (1 x len(series)), con sharey=True.

    Cada panel: una línea con la serie y como título el nombre de la serie.
    La figura lleva el suptitle "Ventas por sucursal".
    """
    raise NotImplementedError("TODO")


def crecimiento_log(anios: list[int], valores: list[float]) -> Figure:
    """Línea de valores con el eje Y en escala logarítmica y ylabel "Valor (escala log)"."""
    raise NotImplementedError("TODO")


def marcar_maximo(x: list[float], y: list[float]) -> Figure:
    """Línea de y contra x, con una anotación (annotate) cuyo texto es "máximo"
    y que señala (xy) el punto más alto, con una flecha (arrowprops).
    Además, una línea horizontal de referencia (axhline) en la media de y.
    """
    raise NotImplementedError("TODO")
