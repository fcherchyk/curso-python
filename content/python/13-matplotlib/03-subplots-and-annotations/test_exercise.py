import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from exercise import log_growth, mark_maximum, panels


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


MONTHS = ["jan", "feb", "mar"]
SERIES = {"North": [10, 12, 9], "South": [100, 120, 130], "Central": [50, 40, 60]}


def test_panels():
    fig = panels(MONTHS, SERIES)
    assert len(fig.axes) == 3
    assert fig.get_suptitle() == "Sales by branch"
    for ax, (name, values) in zip(fig.axes, SERIES.items(), strict=True):
        assert ax.get_title() == name
        assert list(ax.get_lines()[0].get_ydata()) == values
    # in one row: all panels at the same height
    assert len({round(ax.get_position().y0, 3) for ax in fig.axes}) == 1
    # with sharey, the three panels have the same vertical range
    assert len({ax.get_ylim() for ax in fig.axes}) == 1, "use sharey=True"


def test_log_growth():
    fig = log_growth([2020, 2021, 2022], [100, 1000, 10000])
    ax = fig.axes[0]
    assert ax.get_yscale() == "log"
    assert ax.get_ylabel() == "Value (log scale)"
    assert list(ax.get_lines()[0].get_ydata()) == [100, 1000, 10000]


def test_mark_maximum():
    x, y = [1, 2, 3, 4], [5, 9, 7, 3]
    fig = mark_maximum(x, y)
    ax = fig.axes[0]
    annotations = [t for t in ax.texts if isinstance(t, matplotlib.text.Annotation)]
    assert len(annotations) == 1, "use ax.annotate"
    note = annotations[0]
    assert note.get_text() == "maximum"
    assert tuple(note.xy) == (2, 9)
    assert note.arrow_patch is not None, "add the arrow with arrowprops"
    horizontals = [ln for ln in ax.get_lines() if list(ln.get_xdata()) == [0, 1]]
    assert len(horizontals) == 1, "add ax.axhline at the mean"
    assert horizontals[0].get_ydata()[0] == pytest.approx(6)
