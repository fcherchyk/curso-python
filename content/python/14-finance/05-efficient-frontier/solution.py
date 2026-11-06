from pathlib import Path

import matplotlib.pyplot as plt
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
    rng = np.random.default_rng(seed)
    w = rng.random((n_portfolios, n_assets))
    return w / w.sum(axis=1, keepdims=True)


def simulate(returns: pd.DataFrame, n: int, seed: int, risk_free: float = 0.04) -> pd.DataFrame:
    w = random_weights(n, returns.shape[1], seed)
    mu = returns.mean().to_numpy() * TRADING_DAYS
    cov = returns.cov().to_numpy() * TRADING_DAYS
    ret = w @ mu
    vol = np.sqrt(np.einsum("ij,jk,ik->i", w, cov, w))
    sim = pd.DataFrame(w, columns=returns.columns)
    return sim.assign(**{"return": ret, "volatility": vol, "sharpe": (ret - risk_free) / vol})


def max_sharpe(sim: pd.DataFrame) -> pd.Series:
    return sim.loc[sim["sharpe"].idxmax()]


def min_variance(sim: pd.DataFrame) -> pd.Series:
    return sim.loc[sim["volatility"].idxmin()]


def frontier_plot(sim: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    cloud = ax.scatter(sim["volatility"], sim["return"], c=sim["sharpe"], cmap="viridis", s=5)
    fig.colorbar(cloud, ax=ax, label="Sharpe")
    for row, label, marker in [
        (max_sharpe(sim), "Maximum Sharpe", "*"),
        (min_variance(sim), "Minimum variance", "D"),
    ]:
        ax.scatter(row["volatility"], row["return"], marker=marker, s=150, color="red", label=label)
    ax.set(xlabel="Annual volatility", ylabel="Annual return", title="Efficient frontier (Monte Carlo)")
    ax.legend()
    return fig
