import csv
import math
import statistics
from pathlib import Path

import pytest
from exercise import beta, least_correlated, load, sharpe, simple_returns, sortino

# Reference computed without pandas.
with open(Path(__file__).parent / "prices.csv", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))


def rets(col):
    p = [float(row[col]) for row in ROWS]
    return [b / a - 1 for a, b in zip(p[:-1], p[1:], strict=True)]


ACME, INDEX = rets("ACME"), rets("INDEX")
EXCESS = [x - 0.04 / 252 for x in ACME]


@pytest.fixture(scope="module")
def r():
    return simple_returns(load())


def test_sharpe(r):
    s = sharpe(r)
    expected = statistics.mean(EXCESS) / statistics.stdev(ACME) * math.sqrt(252)
    assert s["ACME"] == pytest.approx(expected)
    assert s.idxmax() == "DELTA"
    assert sharpe(r, risk_free=0)["ACME"] > s["ACME"]


def test_sortino(r):
    downside = math.sqrt(statistics.mean(min(x, 0) ** 2 for x in EXCESS)) * math.sqrt(252)
    expected = statistics.mean(EXCESS) * 252 / downside
    assert sortino(r)["ACME"] == pytest.approx(expected)


def test_beta(r):
    b = beta(r)
    assert "INDEX" not in b.index
    expected = statistics.covariance(ACME, INDEX) / statistics.variance(INDEX)
    assert b["ACME"] == pytest.approx(expected)
    assert b.idxmax() == "CIRC" and b.idxmin() == "DELTA"


def test_least_correlated(r):
    assert least_correlated(r, "ACME") == "DELTA"
    candidates = ["ACME", "BETA", "DELTA", "INDEX"]
    expected = min(candidates, key=lambda c: statistics.correlation(rets("CIRC"), rets(c)))
    assert least_correlated(r, "CIRC") == expected
