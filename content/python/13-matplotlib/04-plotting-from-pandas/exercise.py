"""Plotting from pandas. Each function returns the figure (or the Axes, in style_axes)."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "sales.csv"


def load() -> pd.DataFrame:
    """Reads sales.csv with `date` as datetime and adds `amount` = quantity * unit_price."""
    sales = pd.read_csv(CSV, parse_dates=["date"])
    return sales.assign(amount=sales["quantity"] * sales["unit_price"])


def style_axes(ax: Axes, title: str, xlabel: str, ylabel: str) -> Axes:
    """Sets the title and labels, hides the top and right spines,
    and turns on the grid only on the Y axis. Returns the same ax.
    """
    raise NotImplementedError("TODO")


def lines_by_branch(sales: pd.DataFrame) -> Figure:
    """Total amount per month (index: monthly period) and branch (one column each),
    with pivot_table, plotted with df.plot(ax=ax, marker="o").
    Styled with title "Monthly amount by branch", xlabel "Month", ylabel "Amount ($)".
    """
    raise NotImplementedError("TODO")


def bars_by_category(sales: pd.DataFrame) -> Figure:
    """Total amount per category, sorted from smallest to largest, plotted with .plot.barh(ax=ax)
    (the largest ends up at the top). Styled with title "Amount by category",
    xlabel "Amount ($)", ylabel "" (empty).
    """
    raise NotImplementedError("TODO")
