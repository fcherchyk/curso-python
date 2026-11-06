from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def sales_chart(months: list[str], sales: list[float]) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(months, sales, marker="o")
    ax.set(title="Monthly sales", xlabel="Month", ylabel="Sales ($)")
    ax.grid(True, alpha=0.3)
    return fig


def compare_branches(months: list[str], series: dict[str, list[float]]) -> Figure:
    fig, ax = plt.subplots()
    for name, values in series.items():
        ax.plot(months, values, label=name)
    ax.set_title("Sales by branch")
    ax.legend()
    return fig


def save(fig: Figure, path: Path) -> Path:
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
