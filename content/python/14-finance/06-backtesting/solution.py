from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "prices.csv"


def load(asset: str) -> pd.Series:
    return pd.read_csv(CSV, parse_dates=["date"], index_col="date")[asset]


def crossover_signal(prices: pd.Series, short: int = 20, long: int = 50) -> pd.Series:
    return (prices.rolling(short).mean() > prices.rolling(long).mean()).astype(int)


def position(signal: pd.Series) -> pd.Series:
    return signal.shift(1).fillna(0)


def _trades(pos: pd.Series) -> pd.Series:
    return pos.diff().fillna(pos).abs()


def strategy_returns(prices: pd.Series, pos: pd.Series, cost: float = 0.001) -> pd.Series:
    r = prices.pct_change().fillna(0)
    return pos * r - cost * _trades(pos)


def summary(prices: pd.Series, short: int = 20, long: int = 50, cost: float = 0.001) -> dict:
    pos = position(crossover_signal(prices, short, long))
    r_strategy = strategy_returns(prices, pos, cost)
    return {
        "strategy": float((1 + r_strategy).prod() - 1),
        "buy_and_hold": float(prices.iloc[-1] / prices.iloc[0] - 1),
        "trades": int(_trades(pos).sum()),
        "exposure": float(pos.mean()),
    }


def equity_plot(prices: pd.Series, capital: float = 1000, short: int = 20, long: int = 50,
                cost: float = 0.001) -> Figure:
    pos = position(crossover_signal(prices, short, long))
    r = prices.pct_change().fillna(0)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(capital * (1 + strategy_returns(prices, pos, cost)).cumprod(), label="Strategy")
    ax.plot(capital * (1 + r).cumprod(), label="Buy & hold", alpha=0.7)
    ax.set(ylabel="Capital ($)", title=f"Moving-average crossover {short}/{long} vs buy & hold")
    ax.legend()
    return fig
