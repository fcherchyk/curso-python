from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def volatilidad_anual(retornos: pd.DataFrame) -> pd.Series:
    return retornos.std() * np.sqrt(DIAS_HABILES)


def drawdown(precios: pd.DataFrame) -> pd.DataFrame:
    return precios / precios.cummax() - 1


def max_drawdown(precios: pd.DataFrame) -> pd.Series:
    return drawdown(precios).min()


def var_historico(retornos: pd.DataFrame, nivel: float = 0.95) -> pd.Series:
    return -retornos.quantile(1 - nivel)


def cvar_historico(retornos: pd.DataFrame, nivel: float = 0.95) -> pd.Series:
    corte = retornos.quantile(1 - nivel)
    return -retornos[retornos <= corte].mean()
