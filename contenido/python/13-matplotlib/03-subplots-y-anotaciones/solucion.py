import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def paneles(meses: list[str], series: dict[str, list[float]]) -> Figure:
    fig, axs = plt.subplots(1, len(series), sharey=True, squeeze=False, figsize=(10, 3))
    for ax, (nombre, valores) in zip(axs.flat, series.items(), strict=True):
        ax.plot(meses, valores)
        ax.set_title(nombre)
    fig.suptitle("Ventas por sucursal")
    return fig


def crecimiento_log(anios: list[int], valores: list[float]) -> Figure:
    fig, ax = plt.subplots()
    ax.plot(anios, valores)
    ax.set_yscale("log")
    ax.set_ylabel("Valor (escala log)")
    return fig


def marcar_maximo(x: list[float], y: list[float]) -> Figure:
    fig, ax = plt.subplots()
    ax.plot(x, y)
    i = max(range(len(y)), key=y.__getitem__)
    ax.annotate(
        "máximo",
        xy=(x[i], y[i]),
        xytext=(x[i], y[i] * 1.1),
        arrowprops={"arrowstyle": "->"},
    )
    ax.axhline(sum(y) / len(y), color="gray", linestyle=":")
    return fig
