import csv
import math
import statistics
from pathlib import Path

import numpy as np
import pytest
from exercise import (
    annual_volatility,
    drawdown,
    historical_cvar,
    historical_var,
    load,
    max_drawdown,
    simple_returns,
)

# Reference computed without pandas.
with open(Path(__file__).parent / "prices.csv", encoding="utf-8") as f:
    CIRC = [float(row["CIRC"]) for row in csv.DictReader(f)]
R = [b / a - 1 for a, b in zip(CIRC[:-1], CIRC[1:], strict=True)]


def test_annual_volatility():
    vol = annual_volatility(simple_returns(load()))
    assert vol["CIRC"] == pytest.approx(statistics.stdev(R) * math.sqrt(252))
    assert vol.idxmin() == "DELTA"


def test_drawdown():
    dd = drawdown(load())
    peak, expected = CIRC[0], []
    for p in CIRC:
        peak = max(peak, p)
        expected.append(p / peak - 1)
    np.testing.assert_allclose(dd["CIRC"].to_numpy(), expected)
    assert (dd <= 0).all().all()


def test_max_drawdown():
    mdd = max_drawdown(load())
    peak, worst = CIRC[0], 0.0
    for p in CIRC:
        peak = max(peak, p)
        worst = min(worst, p / peak - 1)
    assert mdd["CIRC"] == pytest.approx(worst)
    assert mdd.idxmin() == "CIRC"


def test_historical_var():
    r = simple_returns(load())
    var = historical_var(r)
    assert var["CIRC"] == pytest.approx(-np.quantile(R, 0.05))
    assert var["CIRC"] > 0, "express it as a positive loss"
    assert historical_var(r, 0.99)["CIRC"] > var["CIRC"]


def test_historical_cvar():
    r = simple_returns(load())
    cutoff = np.quantile(R, 0.05)
    tail = [x for x in R if x <= cutoff]
    cvar = historical_cvar(r)
    assert cvar["CIRC"] == pytest.approx(-statistics.mean(tail))
    assert (cvar >= historical_var(r)).all()
