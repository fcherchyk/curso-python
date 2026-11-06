import csv
import math
import statistics
from pathlib import Path

import pandas as pd
import pytest
from exercise import (
    buy_and_hold,
    daily_rebalancing,
    diversification_benefit,
    expected_return,
    load,
    portfolio_return,
    portfolio_volatility,
    simple_returns,
)

ASSETS = ["ACME", "BETA", "CIRC", "DELTA"]
WEIGHTS = {"ACME": 0.4, "BETA": 0.3, "CIRC": 0.1, "DELTA": 0.2}

# Reference computed without pandas.
with open(Path(__file__).parent / "prices.csv", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))
P = {a: [float(row[a]) for row in ROWS] for a in ASSETS}
R = {a: [b / x - 1 for x, b in zip(p[:-1], p[1:], strict=True)] for a, p in P.items()}
R_PORT = [sum(WEIGHTS[a] * R[a][t] for a in ASSETS) for t in range(len(ROWS) - 1)]


@pytest.fixture(scope="module")
def data():
    prices = load()
    return prices, simple_returns(prices), pd.Series(WEIGHTS)


def test_portfolio_return(data):
    _, r, w = data
    rp = portfolio_return(r, w)
    assert list(rp) == pytest.approx(R_PORT)


def test_expected_return(data):
    _, r, w = data
    assert expected_return(r, w) == pytest.approx(statistics.mean(R_PORT) * 252)


def test_portfolio_volatility(data):
    _, r, w = data
    # the variance of the weighted return is exactly wᵀΣw
    assert portfolio_volatility(r, w) == pytest.approx(statistics.stdev(R_PORT) * math.sqrt(252))


def test_diversification_benefit(data):
    _, r, w = data
    average = sum(WEIGHTS[a] * statistics.stdev(R[a]) * math.sqrt(252) for a in ASSETS)
    expected = 1 - statistics.stdev(R_PORT) * math.sqrt(252) / average
    assert diversification_benefit(r, w) == pytest.approx(expected)
    assert diversification_benefit(r, pd.Series({"ACME": 1.0})) == pytest.approx(0, abs=1e-12)


def test_buy_and_hold(data):
    prices, _, w = data
    value, final_weights = buy_and_hold(prices, w, 1000)
    shares = {a: 1000 * WEIGHTS[a] / P[a][0] for a in ASSETS}
    assert value.iloc[0] == pytest.approx(1000)
    assert value.iloc[-1] == pytest.approx(sum(shares[a] * P[a][-1] for a in ASSETS))
    assert final_weights.sum() == pytest.approx(1)
    assert final_weights["ACME"] == pytest.approx(shares["ACME"] * P["ACME"][-1] / value.iloc[-1])


def test_daily_rebalancing(data):
    prices, _, w = data
    value = daily_rebalancing(prices, w, 1000)
    assert len(value) == len(ROWS) - 1
    assert value.index[0] == pd.Timestamp(ROWS[1]["date"])
    assert value.iloc[-1] == pytest.approx(1000 * math.prod(1 + x for x in R_PORT))
