import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def panels(months: list[str], series: dict[str, list[float]]) -> Figure:
    fig, axs = plt.subplots(1, len(series), sharey=True, squeeze=False, figsize=(10, 3))
    for ax, (name, values) in zip(axs.flat, series.items(), strict=True):
        ax.plot(months, values)
        ax.set_title(name)
    fig.suptitle("Sales by branch")
    return fig


def log_growth(years: list[int], values: list[float]) -> Figure:
    fig, ax = plt.subplots()
    ax.plot(years, values)
    ax.set_yscale("log")
    ax.set_ylabel("Value (log scale)")
    return fig


def mark_maximum(x: list[float], y: list[float]) -> Figure:
    fig, ax = plt.subplots()
    ax.plot(x, y)
    i = max(range(len(y)), key=y.__getitem__)
    ax.annotate(
        "maximum",
        xy=(x[i], y[i]),
        xytext=(x[i], y[i] * 1.1),
        arrowprops={"arrowstyle": "->"},
    )
    ax.axhline(sum(y) / len(y), color="gray", linestyle=":")
    return fig
