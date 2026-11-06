"""Medidas de riesgo. `retornos` son retornos simples diarios (una columna por activo)."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def volatilidad_anual(retornos: pd.DataFrame) -> pd.Series:
    """Desvío estándar de los retornos diarios × √252."""
    raise NotImplementedError("TODO")


def drawdown(precios: pd.DataFrame) -> pd.DataFrame:
    """Precio / máximo acumulado hasta esa fecha - 1 (0 en máximos, negativo en caídas)."""
    raise NotImplementedError("TODO")


def max_drawdown(precios: pd.DataFrame) -> pd.Series:
    """La peor caída desde un máximo, por activo (número negativo)."""
    raise NotImplementedError("TODO")


def var_historico(retornos: pd.DataFrame, nivel: float = 0.95) -> pd.Series:
    """VaR histórico como pérdida POSITIVA: -(cuantil 1 - nivel de los retornos)."""
    raise NotImplementedError("TODO")


def cvar_historico(retornos: pd.DataFrame, nivel: float = 0.95) -> pd.Series:
    """Promedio de los retornos <= al cuantil (1 - nivel), como pérdida POSITIVA. Por activo."""
    raise NotImplementedError("TODO")
