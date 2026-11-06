import matplotlib

matplotlib.use("Agg")  # headless: before importing pyplot

import matplotlib.pyplot as plt
import numpy as np
import pytest
from exercise import compare_branches, sales_chart, save

MONTHS = ["jan", "feb", "mar", "apr"]


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_sales_chart():
    fig = sales_chart(MONTHS, [10, 12, 9, 15])
    assert len(fig.axes) == 1
    assert tuple(fig.get_size_inches()) == (8, 4)
    ax = fig.axes[0]
    assert ax.get_title() == "Monthly sales"
    assert ax.get_xlabel() == "Month" and ax.get_ylabel() == "Sales ($)"
    lines = ax.get_lines()
    assert len(lines) == 1
    np.testing.assert_array_equal(lines[0].get_ydata(), [10, 12, 9, 15])
    assert lines[0].get_marker() == "o"
    assert any(line.get_visible() for line in ax.get_xgridlines()), "turn on the grid"


def test_compare_branches():
    fig = compare_branches(MONTHS, {"North": [1, 2, 3, 4], "South": [4, 3, 2, 1]})
    assert len(fig.axes) == 1, "both series go on the same axes"
    ax = fig.axes[0]
    assert ax.get_title() == "Sales by branch"
    assert [line.get_label() for line in ax.get_lines()] == ["North", "South"]
    legend = ax.get_legend()
    assert legend is not None, "the legend is missing"
    assert [t.get_text() for t in legend.get_texts()] == ["North", "South"]


def test_save(tmp_path):
    fig = sales_chart(MONTHS, [1, 2, 3, 4])
    path = save(fig, tmp_path / "sales.png")
    assert path.exists()
    assert path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert not plt.fignum_exists(fig.number), "close the figure after saving"
