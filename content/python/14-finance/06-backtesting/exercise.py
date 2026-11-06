"""Backtesting a moving-average crossover on a single asset (a Series of prices)."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "prices.csv"


def load(asset: str) -> pd.Series:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")[asset]


def crossover_signal(prices: pd.Series, short: int = 20, long: int = 50) -> pd.Series:
    """1 if the short moving average > the long one, 0 otherwise (including days without enough data).
    dtype int.
    """
    raise NotImplementedError("TODO")


def position(signal: pd.Series) -> pd.Series:
    """Each day's position is the PREVIOUS day's signal (no look-ahead). On the first day, 0."""
    raise NotImplementedError("TODO")


def strategy_returns(prices: pd.Series, pos: pd.Series, cost: float = 0.001) -> pd.Series:
    """pos × daily return (pct_change with the first day at 0)
    - cost × |change in position| (the first day's change is the position itself).
    """
    raise NotImplementedError("TODO")


def summary(prices: pd.Series, short: int = 20, long: int = 50, cost: float = 0.001) -> dict:
    """{"strategy": total return, "buy_and_hold": total return,
        "trades": number of position changes (int), "exposure": fraction of days invested}
    """
    raise NotImplementedError("TODO")


def equity_plot(prices: pd.Series, capital: float = 1000, short: int = 20, long: int = 50,
                cost: float = 0.001) -> Figure:
    """Two lines: capital × Π(1 + r_strategy) with label "Strategy" and
    capital × Π(1 + r) with label "Buy & hold". Legend and ylabel "Capital ($)".
    """
    raise NotImplementedError("TODO")
