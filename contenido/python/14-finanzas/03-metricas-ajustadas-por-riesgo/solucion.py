from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def sharpe(retornos: pd.DataFrame, tasa_libre: float = 0.04) -> pd.Series:
    exceso = retornos - tasa_libre / DIAS_HABILES
    return exceso.mean() / retornos.std() * np.sqrt(DIAS_HABILES)


def sortino(retornos: pd.DataFrame, tasa_libre: float = 0.04) -> pd.Series:
    exceso = retornos - tasa_libre / DIAS_HABILES
    desvio_abajo = np.sqrt((exceso.clip(upper=0) ** 2).mean()) * np.sqrt(DIAS_HABILES)
    return exceso.mean() * DIAS_HABILES / desvio_abajo


def beta(retornos: pd.DataFrame, mercado: str = "INDICE") -> pd.Series:
    m = retornos[mercado]
    return retornos.drop(columns=mercado).apply(lambda r: r.cov(m) / m.var())


def menos_correlacionado(retornos: pd.DataFrame, activo: str) -> str:
    return str(retornos.corr()[activo].drop(activo).idxmin())
