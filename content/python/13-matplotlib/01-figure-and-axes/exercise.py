"""Figure and Axes. Use the object-oriented API (fig, ax = plt.subplots()) and return the figure."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
from matplotlib.figure import Figure


def sales_chart(months: list[str], sales: list[float]) -> Figure:
    """Line with "o" markers, an 8x4 inch figure, title "Monthly sales",
    X axis "Month", Y axis "Sales ($)" and the grid turned on.
    """
    raise NotImplementedError("TODO")


def compare_branches(months: list[str], series: dict[str, list[float]]) -> Figure:
    """One line per branch (dict key = label), on the SAME axes, with a legend
    and the title "Sales by branch".
    """
    raise NotImplementedError("TODO")


def save(fig: Figure, path: Path) -> Path:
    """Save the figure as PNG at 150 dpi with bbox_inches="tight", close it and return the path."""
    raise NotImplementedError("TODO")
