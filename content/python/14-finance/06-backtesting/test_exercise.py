import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from exercise import crossover_signal, equity_plot, load, position, strategy_returns, summary

# Reference without pandas: a backtest written with loops.
with open(Path(__file__).parent / "prices.csv", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))


def backtest_by_hand(asset, short, long, cost):
    p = [float(row[asset]) for row in ROWS]
    signal = []
    for t in range(len(p)):
        if t + 1 < long:
            signal.append(0)
        else:
            ma_short = sum(p[t - short + 1 : t + 1]) / short
            ma_long = sum(p[t - long + 1 : t + 1]) / long
            signal.append(1 if ma_short > ma_long else 0)
    pos = [0] + signal[:-1]
    capital, previous, trades = 1.0, 0, 0
    for t in range(1, len(p)):
        change = abs(pos[t] - previous)
        trades += change
        capital *= 1 + pos[t] * (p[t] / p[t - 1] - 1) - cost * change
        previous = pos[t]
    return signal, pos, capital - 1, trades


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_crossover_signal():
    s = crossover_signal(load("ACME"), 20, 50)
    signal, *_ = backtest_by_hand("ACME", 20, 50, 0)
    assert list(s) == signal
    assert s.iloc[:49].eq(0).all(), "without enough data, stay out"


def test_position_without_look_ahead():
    s = pd.Series([1, 0, 1, 1], index=pd.date_range("2025-01-01", periods=4))
    pos = position(s)
    assert list(pos) == [0, 1, 0, 1], "today's position is yesterday's signal"


def test_strategy_returns():
    prices = pd.Series([100.0, 110.0, 99.0, 99.0])
    pos = pd.Series([1, 1, 0, 1])
    r = strategy_returns(prices, pos, cost=0.01)
    # day 0: enters (pays cost); day 1: +10 %; day 2: exits (pays cost); day 3: enters (pays)
    assert list(r) == pytest.approx([-0.01, 0.10, -0.01, -0.01])


@pytest.mark.parametrize("asset", ["ACME", "INDEX"])
def test_summary(asset):
    *_, total, trades = backtest_by_hand(asset, 20, 50, 0.001)
    res = summary(load(asset))
    assert res["strategy"] == pytest.approx(total)
    assert res["trades"] == trades
    p = [float(row[asset]) for row in ROWS]
    assert res["buy_and_hold"] == pytest.approx(p[-1] / p[0] - 1)
    assert 0 < res["exposure"] < 1


def test_costs_subtract():
    acme = load("ACME")
    assert summary(acme, cost=0.01)["strategy"] < summary(acme, cost=0)["strategy"]


def test_equity_plot():
    fig = equity_plot(load("ACME"), capital=1000)
    ax = fig.axes[0]
    assert ax.get_ylabel() == "Capital ($)"
    lines = {ln.get_label(): ln for ln in ax.get_lines()}
    assert set(lines) == {"Strategy", "Buy & hold"}
    *_, total, _ = backtest_by_hand("ACME", 20, 50, 0.001)
    assert lines["Strategy"].get_ydata()[-1] == pytest.approx(1000 * (1 + total))
    p = [float(row["ACME"]) for row in ROWS]
    assert lines["Buy & hold"].get_ydata()[-1] == pytest.approx(1000 * p[-1] / p[0])
    assert not math.isnan(lines["Strategy"].get_ydata()[0])
