import csv
import math
from datetime import date
from pathlib import Path

import pytest
from exercise import (
    annualized_return,
    cagr,
    cumulative_return,
    load,
    log_returns,
    simple_returns,
)

# Reference computed without pandas, using the csv module.
with open(Path(__file__).parent / "prices.csv", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))
ACME = [float(row["ACME"]) for row in ROWS]


def test_simple_returns():
    r = simple_returns(load())
    assert len(r) == len(ROWS) - 1, "drop the first row with dropna()"
    assert not r.isna().any().any()
    assert r["ACME"].iloc[0] == pytest.approx(ACME[1] / ACME[0] - 1)
    assert r["ACME"].iloc[-1] == pytest.approx(ACME[-1] / ACME[-2] - 1)


def test_log_returns():
    r = log_returns(load())
    assert len(r) == len(ROWS) - 1
    assert r["ACME"].iloc[0] == pytest.approx(math.log(ACME[1] / ACME[0]))
    assert r["ACME"].sum() == pytest.approx(math.log(ACME[-1] / ACME[0])), "log returns add up"


def test_cumulative_return():
    cum = cumulative_return(simple_returns(load()))
    assert cum["ACME"] == pytest.approx(ACME[-1] / ACME[0] - 1)
    assert cum["BETA"] < 0


def test_annualized_return():
    annual = annualized_return(simple_returns(load()))
    n = len(ACME) - 1
    assert annual["ACME"] == pytest.approx((ACME[-1] / ACME[0]) ** (252 / n) - 1)


def test_cagr():
    c = cagr(load())
    years = (date.fromisoformat(ROWS[-1]["date"]) - date.fromisoformat(ROWS[0]["date"])).days / 365.25
    assert c["ACME"] == pytest.approx((ACME[-1] / ACME[0]) ** (1 / years) - 1)
    assert set(c.index) == {"ACME", "BETA", "CIRC", "DELTA", "INDEX"}
