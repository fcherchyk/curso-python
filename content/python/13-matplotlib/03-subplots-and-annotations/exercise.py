"""Subplots, scales and annotations. Each function returns the figure."""

import matplotlib.pyplot as plt  # noqa: F401
from matplotlib.figure import Figure


def panels(months: list[str], series: dict[str, list[float]]) -> Figure:
    """One panel per series, in ONE row (1 x len(series)), with sharey=True.

    Each panel: a line with the series and the series name as its title.
    The figure gets the suptitle "Sales by branch".
    """
    raise NotImplementedError("TODO")


def log_growth(years: list[int], values: list[float]) -> Figure:
    """Line of values with the Y axis on a logarithmic scale and ylabel "Value (log scale)"."""
    raise NotImplementedError("TODO")


def mark_maximum(x: list[float], y: list[float]) -> Figure:
    """Line of y against x, with an annotation (annotate) whose text is "maximum"
    and that points (xy) at the highest point, with an arrow (arrowprops).
    Also, a horizontal reference line (axhline) at the mean of y.
    """
    raise NotImplementedError("TODO")
