"""Risk-adjusted metrics. `returns`: daily simple returns, one column per asset."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def sharpe(returns: pd.DataFrame, risk_free: float = 0.04) -> pd.Series:
    """excess = returns - risk_free / 252;  mean(excess) / std(returns) × √252."""
    raise NotImplementedError("TODO")


def sortino(returns: pd.DataFrame, risk_free: float = 0.04) -> pd.Series:
    """mean(excess) × 252 / downside_deviation, with
    downside_deviation = √(mean(min(excess, 0)²)) × √252 (over ALL days).
    """
    raise NotImplementedError("TODO")


def beta(returns: pd.DataFrame, market: str = "INDEX") -> pd.Series:
    """cov(asset, market) / var(market) for every column EXCEPT the market."""
    raise NotImplementedError("TODO")


def least_correlated(returns: pd.DataFrame, asset: str) -> str:
    """The name of the other column with the lowest correlation with `asset`."""
    raise NotImplementedError("TODO")
