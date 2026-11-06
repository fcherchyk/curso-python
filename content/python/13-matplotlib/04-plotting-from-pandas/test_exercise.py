import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from exercise import bars_by_category, lines_by_branch, load, style_axes


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def totals(key):
    """Reference computed without pandas, with the csv module."""
    acc = defaultdict(int)
    with open(Path(__file__).parent / "sales.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            acc[key(row)] += int(row["quantity"]) * int(row["unit_price"])
    return acc


def test_style_axes():
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    returned = style_axes(ax, "T", "X", "Y")
    assert returned is ax
    assert (ax.get_title(), ax.get_xlabel(), ax.get_ylabel()) == ("T", "X", "Y")
    assert not ax.spines["top"].get_visible() and not ax.spines["right"].get_visible()
    assert ax.spines["left"].get_visible() and ax.spines["bottom"].get_visible()
    assert any(g.get_visible() for g in ax.yaxis.get_gridlines()), "grid on Y"
    assert not any(g.get_visible() for g in ax.xaxis.get_gridlines()), "no grid on X"


def test_lines_by_branch():
    fig = lines_by_branch(load())
    ax = fig.axes[0]
    assert ax.get_title() == "Monthly amount by branch"
    assert ax.get_ylabel() == "Amount ($)"
    assert not ax.spines["top"].get_visible(), "apply style_axes"
    ref = totals(lambda r: (r["branch"], r["date"][:7]))
    legend = [t.get_text() for t in ax.get_legend().get_texts()]
    assert sorted(legend) == ["Central", "North", "South"]
    for line, branch in zip(ax.get_lines(), legend, strict=True):
        assert line.get_marker() == "o"
        expected = [ref[(branch, m)] for m in ("2025-01", "2025-02", "2025-03")]
        assert list(line.get_ydata()) == expected, branch


def test_bars_by_category():
    fig = bars_by_category(load())
    ax = fig.axes[0]
    assert ax.get_title() == "Amount by category"
    assert ax.get_xlabel() == "Amount ($)" and ax.get_ylabel() == ""
    assert not ax.spines["right"].get_visible(), "apply style_axes"
    ref = totals(lambda r: r["category"])
    expected = sorted(ref.items(), key=lambda kv: kv[1])
    assert [t.get_text() for t in ax.get_yticklabels()] == [k for k, _ in expected]
    assert [b.get_width() for b in ax.patches] == [v for _, v in expected]
