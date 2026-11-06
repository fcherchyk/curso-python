from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "prices.csv"
ASSETS = ["ACME", "BETA", "CIRC", "DELTA"]
TRADING_DAYS = 252


def load() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")[ASSETS]


def simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()


def portfolio_return(returns: pd.DataFrame, weights: pd.Series) -> pd.Series:
    return returns[weights.index] @ weights


def expected_return(returns: pd.DataFrame, weights: pd.Series) -> float:
    return float(weights @ returns[weights.index].mean() * TRADING_DAYS)


def portfolio_volatility(returns: pd.DataFrame, weights: pd.Series) -> float:
    cov = returns[weights.index].cov() * TRADING_DAYS
    return float(np.sqrt(weights @ cov @ weights))


def diversification_benefit(returns: pd.DataFrame, weights: pd.Series) -> float:
    individual_vol = returns[weights.index].std() * np.sqrt(TRADING_DAYS)
    return 1 - portfolio_volatility(returns, weights) / float(weights @ individual_vol)


def buy_and_hold(prices: pd.DataFrame, weights: pd.Series, capital: float) -> tuple[pd.Series, pd.Series]:
    prices = prices[weights.index]
    shares = capital * weights / prices.iloc[0]
    holdings = prices * shares
    value = holdings.sum(axis=1)
    return value, holdings.iloc[-1] / value.iloc[-1]


def daily_rebalancing(prices: pd.DataFrame, weights: pd.Series, capital: float) -> pd.Series:
    return capital * (1 + portfolio_return(simple_returns(prices), weights)).cumprod()
