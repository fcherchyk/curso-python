"""Risk measures. `returns` are daily simple returns (one column per asset)."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def annual_volatility(returns: pd.DataFrame) -> pd.Series:
    """Standard deviation of daily returns × √252."""
    raise NotImplementedError("TODO")


def drawdown(prices: pd.DataFrame) -> pd.DataFrame:
    """Price / running maximum up to that date - 1 (0 at peaks, negative during falls)."""
    raise NotImplementedError("TODO")


def max_drawdown(prices: pd.DataFrame) -> pd.Series:
    """The worst fall from a peak, per asset (a negative number)."""
    raise NotImplementedError("TODO")


def historical_var(returns: pd.DataFrame, level: float = 0.95) -> pd.Series:
    """Historical VaR as a POSITIVE loss: -(the 1 - level quantile of the returns)."""
    raise NotImplementedError("TODO")


def historical_cvar(returns: pd.DataFrame, level: float = 0.95) -> pd.Series:
    """Average of the returns <= the (1 - level) quantile, as a POSITIVE loss. Per asset."""
    raise NotImplementedError("TODO")
