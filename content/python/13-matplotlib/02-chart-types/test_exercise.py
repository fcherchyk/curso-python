import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest
from exercise import histogram, recommended_chart, scatter_plot, sorted_bars


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_sorted_bars():
    fig = sorted_bars({"North": 245, "South": 380, "Central": 230}, "Revenue")
    ax = fig.axes[0]
    assert ax.get_title() == "Revenue"
    bars = ax.patches
    assert len(bars) == 3
    widths = [b.get_width() for b in bars]  # in barh, the value is the width
    assert widths == [230, 245, 380], "smallest to largest, so the largest ends up at the top"
    labels = [t.get_text() for t in ax.get_yticklabels()]
    assert labels == ["Central", "North", "South"]
    assert len(ax.texts) == 3, "add the values with bar_label"


def test_scatter_plot():
    fig = scatter_plot([1, 2, 3], [2, 4, 7], "Advertising", "Sales")
    ax = fig.axes[0]
    points = ax.collections[0]
    np.testing.assert_array_equal(points.get_offsets(), [[1, 2], [2, 4], [3, 7]])
    assert points.get_alpha() == pytest.approx(0.6)
    assert (ax.get_xlabel(), ax.get_ylabel()) == ("Advertising", "Sales")


def test_histogram():
    values = np.random.default_rng(0).normal(10, 2, 500)
    fig = histogram(values, 25)
    ax = fig.axes[0]
    assert len(ax.patches) == 25
    assert sum(b.get_height() for b in ax.patches) == 500
    lines = ax.get_lines()
    assert len(lines) == 1 and lines[0].get_linestyle() == "--"
    assert lines[0].get_xdata()[0] == pytest.approx(values.mean())
    assert ax.get_legend() is not None


def test_recommended_chart():
    assert recommended_chart("trend") == "line"
    assert recommended_chart("comparison") == "bar"
    assert recommended_chart("relationship") == "scatter"
    assert recommended_chart("distribution") == "histogram"
    with pytest.raises(ValueError):
        recommended_chart("share of the pie")
