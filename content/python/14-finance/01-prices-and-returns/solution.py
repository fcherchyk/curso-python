from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1)).dropna()


def cumulative_return(returns: pd.DataFrame) -> pd.Series:
    return (1 + returns).prod() - 1


def annualized_return(returns: pd.DataFrame) -> pd.Series:
    return (1 + cumulative_return(returns)) ** (TRADING_DAYS / len(returns)) - 1


def cagr(prices: pd.DataFrame) -> pd.Series:
    years = (prices.index[-1] - prices.index[0]).days / 365.25
    return (prices.iloc[-1] / prices.iloc[0]) ** (1 / years) - 1
