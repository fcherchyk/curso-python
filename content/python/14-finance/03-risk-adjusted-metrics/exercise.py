"""Métricas ajustadas por riesgo. `retornos`: retornos simples diarios, una columna por activo."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def sharpe(retornos: pd.DataFrame, tasa_libre: float = 0.04) -> pd.Series:
    """exceso = retornos - tasa_libre / 252;  media(exceso) / desvío(retornos) × √252."""
    raise NotImplementedError("TODO")


def sortino(retornos: pd.DataFrame, tasa_libre: float = 0.04) -> pd.Series:
    """media(exceso) × 252 / desvío_a_la_baja, con
    desvío_a_la_baja = √(media(min(exceso, 0)²)) × √252 (sobre TODOS los días).
    """
    raise NotImplementedError("TODO")


def beta(retornos: pd.DataFrame, mercado: str = "INDICE") -> pd.Series:
    """cov(activo, mercado) / var(mercado) para cada columna EXCEPTO el mercado."""
    raise NotImplementedError("TODO")


def menos_correlacionado(retornos: pd.DataFrame, activo: str) -> str:
    """El nombre de la otra columna con menor correlación con `activo`."""
    raise NotImplementedError("TODO")
