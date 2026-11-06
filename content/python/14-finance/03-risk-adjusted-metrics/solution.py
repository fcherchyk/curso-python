from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def sharpe(returns: pd.DataFrame, risk_free: float = 0.04) -> pd.Series:
    excess = returns - risk_free / TRADING_DAYS
    return excess.mean() / returns.std() * np.sqrt(TRADING_DAYS)


def sortino(returns: pd.DataFrame, risk_free: float = 0.04) -> pd.Series:
    excess = returns - risk_free / TRADING_DAYS
    downside_dev = np.sqrt((excess.clip(upper=0) ** 2).mean()) * np.sqrt(TRADING_DAYS)
    return excess.mean() * TRADING_DAYS / downside_dev


def beta(returns: pd.DataFrame, market: str = "INDEX") -> pd.Series:
    m = returns[market]
    return returns.drop(columns=market).apply(lambda r: r.cov(m) / m.var())


def least_correlated(returns: pd.DataFrame, asset: str) -> str:
    return str(returns.corr()[asset].drop(asset).idxmin())
