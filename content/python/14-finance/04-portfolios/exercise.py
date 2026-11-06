"""Portfolios. `weights` is a Series indexed by asset whose values add up to 1."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
ASSETS = ["ACME", "BETA", "CIRC", "DELTA"]
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    """Only the four stocks (without INDEX)."""
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")[ASSETS]


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def portfolio_return(returns: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Daily return of the portfolio with fixed weights: Σ wᵢ·rᵢ."""
    raise NotImplementedError("TODO")


def expected_return(returns: pd.DataFrame, weights: pd.Series) -> float:
    """Expected annual return: weights · daily mean × 252."""
    raise NotImplementedError("TODO")


def portfolio_volatility(returns: pd.DataFrame, weights: pd.Series) -> float:
    """√(wᵀ Σ w) with Σ = daily covariance × 252."""
    raise NotImplementedError("TODO")


def diversification_benefit(returns: pd.DataFrame, weights: pd.Series) -> float:
    """1 - portfolio vol / weighted average of the individual annual vols."""
    raise NotImplementedError("TODO")


def buy_and_hold(prices: pd.DataFrame, weights: pd.Series, capital: float) -> tuple[pd.Series, pd.Series]:
    """Buy on the first day (capital × weight / initial price shares of each asset) and never
    trade again. Return (daily portfolio value, weights on the last day).
    """
    raise NotImplementedError("TODO")


def daily_rebalancing(prices: pd.DataFrame, weights: pd.Series, capital: float) -> pd.Series:
    """Portfolio value rebalancing every day: capital × Π(1 + portfolio return).
    The index starts at the SECOND date (that of the first return).
    """
    raise NotImplementedError("TODO")
