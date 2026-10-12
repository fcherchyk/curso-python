import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

RECOMENDADOS = {
    "evolucion": "linea",
    "comparacion": "barras",
    "relacion": "dispersion",
    "distribucion": "histograma",
}


def barras_ordenadas(totales: dict[str, float], titulo: str) -> Figure:
    ordenados = sorted(totales.items(), key=lambda kv: kv[1])  # menor abajo, mayor arriba
    fig, ax = plt.subplots()
    barras = ax.barh([k for k, _ in ordenados], [v for _, v in ordenados])
    ax.bar_label(barras, fmt="%.0f")
    ax.set_title(titulo)
    return fig


def dispersion(x: list[float], y: list[float], xlabel: str, ylabel: str) -> Figure:
    fig, ax = plt.subplots()
    ax.scatter(x, y, alpha=0.6)
    ax.set(xlabel=xlabel, ylabel=ylabel)
    return fig


def histograma(valores: np.ndarray, bins: int) -> Figure:
    fig, ax = plt.subplots()
    ax.hist(valores, bins=bins, edgecolor="white")
    ax.axvline(valores.mean(), linestyle="--", color="red", label="media")
    ax.legend()
    return fig


def tipo_recomendado(pregunta: str) -> str:
    try:
        return RECOMENDADOS[pregunta]
    except KeyError:
        raise ValueError(f"pregunta desconocida: {pregunta!r}") from None
