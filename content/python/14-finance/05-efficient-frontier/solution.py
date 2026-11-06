from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "precios.csv"
ACTIVOS = ["ACME", "BETA", "CIRC", "DELTA"]
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")[ACTIVOS]


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def pesos_aleatorios(n_portafolios: int, n_activos: int, semilla: int) -> np.ndarray:
    rng = np.random.default_rng(semilla)
    w = rng.random((n_portafolios, n_activos))
    return w / w.sum(axis=1, keepdims=True)


def simular(retornos: pd.DataFrame, n: int, semilla: int, tasa_libre: float = 0.04) -> pd.DataFrame:
    w = pesos_aleatorios(n, retornos.shape[1], semilla)
    mu = retornos.mean().to_numpy() * DIAS_HABILES
    cov = retornos.cov().to_numpy() * DIAS_HABILES
    ret = w @ mu
    vol = np.sqrt(np.einsum("ij,jk,ik->i", w, cov, w))
    sim = pd.DataFrame(w, columns=retornos.columns)
    return sim.assign(retorno=ret, volatilidad=vol, sharpe=(ret - tasa_libre) / vol)


def max_sharpe(sim: pd.DataFrame) -> pd.Series:
    return sim.loc[sim["sharpe"].idxmax()]


def min_varianza(sim: pd.DataFrame) -> pd.Series:
    return sim.loc[sim["volatilidad"].idxmin()]


def grafico_frontera(sim: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    nube = ax.scatter(sim["volatilidad"], sim["retorno"], c=sim["sharpe"], cmap="viridis", s=5)
    fig.colorbar(nube, ax=ax, label="Sharpe")
    for fila, label, marca in [
        (max_sharpe(sim), "Máximo Sharpe", "*"),
        (min_varianza(sim), "Mínima varianza", "D"),
    ]:
        ax.scatter(fila["volatilidad"], fila["retorno"], marker=marca, s=150, color="red", label=label)
    ax.set(xlabel="Volatilidad anual", ylabel="Retorno anual", title="Frontera eficiente (Monte Carlo)")
    ax.legend()
    return fig
