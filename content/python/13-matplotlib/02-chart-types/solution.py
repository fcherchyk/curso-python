import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

RECOMMENDED = {
    "trend": "line",
    "comparison": "bar",
    "relationship": "scatter",
    "distribution": "histogram",
}


def sorted_bars(totals: dict[str, float], title: str) -> Figure:
    ordered = sorted(totals.items(), key=lambda kv: kv[1])  # smallest at the bottom, largest at the top
    fig, ax = plt.subplots()
    bars = ax.barh([k for k, _ in ordered], [v for _, v in ordered])
    ax.bar_label(bars, fmt="%.0f")
    ax.set_title(title)
    return fig


def scatter_plot(x: list[float], y: list[float], xlabel: str, ylabel: str) -> Figure:
    fig, ax = plt.subplots()
    ax.scatter(x, y, alpha=0.6)
    ax.set(xlabel=xlabel, ylabel=ylabel)
    return fig


def histogram(values: np.ndarray, bins: int) -> Figure:
    fig, ax = plt.subplots()
    ax.hist(values, bins=bins, edgecolor="white")
    ax.axvline(values.mean(), linestyle="--", color="red", label="mean")
    ax.legend()
    return fig


def recommended_chart(question: str) -> str:
    try:
        return RECOMMENDED[question]
    except KeyError:
        raise ValueError(f"unknown question: {question!r}") from None
