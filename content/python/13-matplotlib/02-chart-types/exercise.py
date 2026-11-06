"""Chart types. Object-oriented API; each function returns the figure."""

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np  # noqa: F401
from matplotlib.figure import Figure


def sorted_bars(totals: dict[str, float], title: str) -> Figure:
    """HORIZONTAL bars (barh) sorted so the LARGEST ends up at the TOP,
    with the value on each bar (bar_label) and the given title.

    Hint: in barh, the first bar goes at the bottom; sort from smallest to largest.
    """
    raise NotImplementedError("TODO")


def scatter_plot(x: list[float], y: list[float], xlabel: str, ylabel: str) -> Figure:
    """Scatter with alpha=0.6 and the axis labels."""
    raise NotImplementedError("TODO")


def histogram(values: np.ndarray, bins: int) -> Figure:
    """Histogram with `bins` bars and a dashed vertical line (axvline, "--") at the mean,
    with label "mean" and a legend.
    """
    raise NotImplementedError("TODO")


def recommended_chart(question: str) -> str:
    """Based on the question: "trend" → "line", "comparison" → "bar",
    "relationship" → "scatter", "distribution" → "histogram". Anything else → ValueError.
    """
    raise NotImplementedError("TODO")
