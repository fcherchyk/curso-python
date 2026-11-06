import csv
from datetime import date

import pandas as pd
import pytest
from exercise import (
    bullish_crossovers,
    load_prices,
    monthly_closes,
    monthly_returns,
    yearly_performance,
)

# Pure Python reference: date → ACME price
with open("prices.csv", newline="", encoding="utf-8") as f:
    ACME = [(date.fromisoformat(r["date"]), float(r["ACME"])) for r in csv.DictReader(f)]


def last_of(year: int, month: int | None = None) -> float:
    return [p for d, p in ACME if d.year == year and (month is None or d.month == month)][-1]


@pytest.fixture(scope="module")
def prices():
    return load_prices("prices.csv")


def test_load_prices(prices):
    assert isinstance(prices.index, pd.DatetimeIndex)
    assert prices.index.name == "date"
    assert list(prices.columns) == ["ACME", "BETA", "CIRC", "DELTA", "INDEX"]


def test_monthly_closes(prices):
    m = monthly_closes(prices)
    assert len(m) == 36
    assert m.loc["2024-03", "ACME"].iloc[0] == last_of(2024, 3)


def test_monthly_returns(prices):
    r = monthly_returns(prices)
    assert len(r) == 35
    assert not r.isna().any().any()
    expected = last_of(2024, 3) / last_of(2024, 2) - 1
    assert r.loc["2024-03", "ACME"].iloc[0] == pytest.approx(expected)


def test_yearly_performance(prices):
    r = yearly_performance(prices, "ACME")
    assert set(r) == {2023, 2024, 2025}
    assert r[2023] == round(last_of(2023) / ACME[0][1] - 1, 4)
    assert r[2025] == round(last_of(2025) / last_of(2024) - 1, 4)


def test_bullish_crossovers(prices):
    crossovers = bullish_crossovers(prices["ACME"], 20, 50)
    assert crossovers, "there must be at least one crossover"
    dates = [d for d, _ in ACME]
    values = [p for _, p in ACME]

    def mean(end: int, n: int) -> float:
        return sum(values[end - n + 1 : end + 1]) / n

    for c in crossovers:
        i = dates.index(c.date())
        assert i >= 50, "there can't be crossovers before having 50 data points"
        assert mean(i, 20) > mean(i, 50)
        assert mean(i - 1, 20) <= mean(i - 1, 50)
