"""Efficient frontier with Monte Carlo, using vectorized NumPy."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "prices.csv"
ASSETS = ["ACME", "BETA", "CIRC", "DELTA"]
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")[ASSETS]


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def random_weights(n_portfolios: int, n_assets: int, seed: int) -> np.ndarray:
    """Matrix (n_portfolios, n_assets): rng = default_rng(seed), rng.random(...),
    with each row normalized so it adds up to 1.
    """
    raise NotImplementedError("TODO")


def simulate(returns: pd.DataFrame, n: int, seed: int, risk_free: float = 0.04) -> pd.DataFrame:
    """A DataFrame with n rows and columns: one per asset (the weights), "return" (annual),
    "volatility" (annual) and "sharpe" ((return - risk_free) / volatility).
    No loops: use W @ mu and einsum (or ((W @ cov) * W).sum(axis=1)).
    """
    raise NotImplementedError("TODO")


def max_sharpe(sim: pd.DataFrame) -> pd.Series:
    """The row with the highest Sharpe."""
    raise NotImplementedError("TODO")


def min_variance(sim: pd.DataFrame) -> pd.Series:
    """The row with the lowest volatility."""
    raise NotImplementedError("TODO")


def frontier_plot(sim: pd.DataFrame) -> Figure:
    """Scatter of volatility (X) vs return (Y) colored by sharpe (c=..., cmap="viridis").
    On top, two points: max_sharpe (label "Maximum Sharpe") and min_variance
    (label "Minimum variance"), each with its own scatter. Legend.
    xlabel "Annual volatility", ylabel "Annual return".
    """
    raise NotImplementedError("TODO")
