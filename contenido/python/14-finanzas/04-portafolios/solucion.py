from pathlib import Path

import numpy as np
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
ACTIVOS = ["ACME", "BETA", "CIRC", "DELTA"]
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")[ACTIVOS]


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def retorno_portafolio(retornos: pd.DataFrame, pesos: pd.Series) -> pd.Series:
    return retornos[pesos.index] @ pesos


def retorno_esperado(retornos: pd.DataFrame, pesos: pd.Series) -> float:
    return float(pesos @ retornos[pesos.index].mean() * DIAS_HABILES)


def volatilidad_portafolio(retornos: pd.DataFrame, pesos: pd.Series) -> float:
    cov = retornos[pesos.index].cov() * DIAS_HABILES
    return float(np.sqrt(pesos @ cov @ pesos))


def beneficio_diversificacion(retornos: pd.DataFrame, pesos: pd.Series) -> float:
    vol_individual = retornos[pesos.index].std() * np.sqrt(DIAS_HABILES)
    return 1 - volatilidad_portafolio(retornos, pesos) / float(pesos @ vol_individual)


def buy_and_hold(precios: pd.DataFrame, pesos: pd.Series, capital: float) -> tuple[pd.Series, pd.Series]:
    precios = precios[pesos.index]
    acciones = capital * pesos / precios.iloc[0]
    tenencias = precios * acciones
    valor = tenencias.sum(axis=1)
    return valor, tenencias.iloc[-1] / valor.iloc[-1]


def rebalanceo_diario(precios: pd.DataFrame, pesos: pd.Series, capital: float) -> pd.Series:
    return capital * (1 + retorno_portafolio(retornos_simples(precios), pesos)).cumprod()
