from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def annual_volatility(returns: pd.DataFrame) -> pd.Series:
    return returns.std() * np.sqrt(TRADING_DAYS)


def drawdown(prices: pd.DataFrame) -> pd.DataFrame:
    return prices / prices.cummax() - 1


def max_drawdown(prices: pd.DataFrame) -> pd.Series:
    return drawdown(prices).min()


def historical_var(returns: pd.DataFrame, level: float = 0.95) -> pd.Series:
    return -returns.quantile(1 - level)


def historical_cvar(returns: pd.DataFrame, level: float = 0.95) -> pd.Series:
    cutoff = returns.quantile(1 - level)
    return -returns[returns <= cutoff].mean()
