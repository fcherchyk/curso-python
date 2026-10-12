from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def retornos_log(precios: pd.DataFrame) -> pd.DataFrame:
    return np.log(precios / precios.shift(1)).dropna()


def retorno_acumulado(retornos: pd.DataFrame) -> pd.Series:
    return (1 + retornos).prod() - 1


def retorno_anualizado(retornos: pd.DataFrame) -> pd.Series:
    return (1 + retorno_acumulado(retornos)) ** (DIAS_HABILES / len(retornos)) - 1


def cagr(precios: pd.DataFrame) -> pd.Series:
    anios = (precios.index[-1] - precios.index[0]).days / 365.25
    return (precios.iloc[-1] / precios.iloc[0]) ** (1 / anios) - 1
