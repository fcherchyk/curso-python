"""Tipos de gráfico. API orientada a objetos; cada función devuelve la figura."""

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np  # noqa: F401
from matplotlib.figure import Figure


def barras_ordenadas(totales: dict[str, float], titulo: str) -> Figure:
    """Barras HORIZONTALES (barh) ordenadas de forma que la MAYOR quede ARRIBA,
    con el valor sobre cada barra (bar_label) y el título dado.

    Pista: en barh, la primera barra va abajo; ordená de menor a mayor.
    """
    raise NotImplementedError("TODO")


def dispersion(x: list[float], y: list[float], xlabel: str, ylabel: str) -> Figure:
    """Scatter con alpha=0.6 y las etiquetas de los ejes."""
    raise NotImplementedError("TODO")


def histograma(valores: np.ndarray, bins: int) -> Figure:
    """Histograma con `bins` barras y una línea vertical punteada (axvline, "--") en la media,
    con label "media" y leyenda.
    """
    raise NotImplementedError("TODO")


def tipo_recomendado(pregunta: str) -> str:
    """Según la pregunta: "evolucion" → "linea", "comparacion" → "barras",
    "relacion" → "dispersion", "distribucion" → "histograma". Otra → ValueError.
    """
    raise NotImplementedError("TODO")
