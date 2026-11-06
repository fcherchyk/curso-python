from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "sales.csv"


def load() -> pd.DataFrame:
    sales = pd.read_csv(CSV, parse_dates=["date"])
    return sales.assign(amount=sales["quantity"] * sales["unit_price"])


def style_axes(ax: Axes, title: str, xlabel: str, ylabel: str) -> Axes:
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    return ax


def lines_by_branch(sales: pd.DataFrame) -> Figure:
    monthly = sales.assign(month=sales["date"].dt.to_period("M")).pivot_table(
        index="month", columns="branch", values="amount", aggfunc="sum"
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    monthly.plot(ax=ax, marker="o")
    style_axes(ax, "Monthly amount by branch", "Month", "Amount ($)")
    return fig


def bars_by_category(sales: pd.DataFrame) -> Figure:
    by_category = sales.groupby("category")["amount"].sum().sort_values()
    fig, ax = plt.subplots()
    by_category.plot.barh(ax=ax)
    style_axes(ax, "Amount by category", "Amount ($)", "")
    return fig
