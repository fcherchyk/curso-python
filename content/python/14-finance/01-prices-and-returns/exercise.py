"""Prices and returns. `prices` is a DataFrame with a date index and one column per asset."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """P_t / P_{t-1} - 1, without the first row (NaN)."""
    raise NotImplementedError("TODO")


def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """ln(P_t / P_{t-1}), without the first row."""
    raise NotImplementedError("TODO")


def cumulative_return(returns: pd.DataFrame) -> pd.Series:
    """Total return over the period per asset, compounding the simple returns."""
    raise NotImplementedError("TODO")


def annualized_return(returns: pd.DataFrame) -> pd.Series:
    """(1 + cumulative) ** (252 / number of returns) - 1, per asset."""
    raise NotImplementedError("TODO")


def cagr(prices: pd.DataFrame) -> pd.Series:
    """(last / first) ** (1 / years) - 1, with years = calendar days / 365.25."""
    raise NotImplementedError("TODO")
