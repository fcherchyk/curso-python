import csv
import math
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest
from exercise import (
    frontier_plot,
    load,
    max_sharpe,
    min_variance,
    random_weights,
    simple_returns,
    simulate,
)

ASSETS = ["ACME", "BETA", "CIRC", "DELTA"]

# Reference without pandas.
with open(Path(__file__).parent / "prices.csv", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))
P = {a: [float(row[a]) for row in ROWS] for a in ASSETS}
R = {a: [b / x - 1 for x, b in zip(p[:-1], p[1:], strict=True)] for a, p in P.items()}


def ref(weights):
    """Annual return and volatility of a portfolio, summing by hand."""
    rp = [sum(w * R[a][t] for a, w in zip(ASSETS, weights, strict=True)) for t in range(len(ROWS) - 1)]
    return statistics.mean(rp) * 252, statistics.stdev(rp) * math.sqrt(252)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


@pytest.fixture(scope="module")
def sim():
    return simulate(simple_returns(load()), 2000, seed=7)


def test_random_weights():
    w = random_weights(100, 4, seed=1)
    assert w.shape == (100, 4)
    np.testing.assert_allclose(w.sum(axis=1), 1)
    assert (w >= 0).all()
    raw = np.random.default_rng(1).random((100, 4))
    np.testing.assert_allclose(w, raw / raw.sum(axis=1, keepdims=True))
    assert not np.allclose(w, random_weights(100, 4, seed=2))


def test_simulate(sim):
    assert len(sim) == 2000
    assert set(ASSETS + ["return", "volatility", "sharpe"]) <= set(sim.columns)
    for i in (0, 1234):
        row = sim.iloc[i]
        ret, vol = ref([row[a] for a in ASSETS])
        assert row["return"] == pytest.approx(ret)
        assert row["volatility"] == pytest.approx(vol)
        assert row["sharpe"] == pytest.approx((ret - 0.04) / vol)


def test_max_sharpe_and_min_variance(sim):
    best = max_sharpe(sim)
    least_risk = min_variance(sim)
    assert best["sharpe"] == pytest.approx(sim["sharpe"].max())
    assert least_risk["volatility"] == pytest.approx(sim["volatility"].min())
    assert best["DELTA"] > 0.5, "DELTA dominates: low vol, good return and little correlation"


def test_frontier_plot(sim):
    fig = frontier_plot(sim)
    ax = fig.axes[0]
    assert (ax.get_xlabel(), ax.get_ylabel()) == ("Annual volatility", "Annual return")
    cloud, *highlighted = ax.collections
    assert len(cloud.get_offsets()) == 2000
    np.testing.assert_allclose(cloud.get_array(), sim["sharpe"])
    legend = {t.get_text() for t in ax.get_legend().get_texts()}
    assert legend == {"Maximum Sharpe", "Minimum variance"}
    points = {tuple(np.round(c.get_offsets()[0], 10)) for c in highlighted}
    best = max_sharpe(sim)
    assert (round(best["volatility"], 10), round(best["return"], 10)) in points
