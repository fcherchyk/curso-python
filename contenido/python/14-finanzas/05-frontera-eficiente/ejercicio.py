"""Frontera eficiente por Monte Carlo, con NumPy vectorizado."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
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
    """Matriz (n_portafolios, n_activos): rng = default_rng(semilla), rng.random(...),
    y cada fila normalizada para que sume 1.
    """
    raise NotImplementedError("TODO")


def simular(retornos: pd.DataFrame, n: int, semilla: int, tasa_libre: float = 0.04) -> pd.DataFrame:
    """Un DataFrame de n filas con columnas: una por activo (los pesos), "retorno" (anual),
    "volatilidad" (anual) y "sharpe" ((retorno - tasa_libre) / volatilidad).
    Sin bucles: usá W @ mu y einsum (o ((W @ cov) * W).sum(axis=1)).
    """
    raise NotImplementedError("TODO")


def max_sharpe(sim: pd.DataFrame) -> pd.Series:
    """La fila con mayor Sharpe."""
    raise NotImplementedError("TODO")


def min_varianza(sim: pd.DataFrame) -> pd.Series:
    """La fila con menor volatilidad."""
    raise NotImplementedError("TODO")


def grafico_frontera(sim: pd.DataFrame) -> Figure:
    """Scatter volatilidad (X) vs retorno (Y) coloreado por sharpe (c=..., cmap="viridis").
    Encima, dos puntos: max_sharpe (label "Máximo Sharpe") y min_varianza
    (label "Mínima varianza"), cada uno con su propio scatter. Leyenda.
    xlabel "Volatilidad anual", ylabel "Retorno anual".
    """
    raise NotImplementedError("TODO")
