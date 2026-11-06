"""Portafolios. `pesos` es una Series indexada por activo cuyos valores suman 1."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
ACTIVOS = ["ACME", "BETA", "CIRC", "DELTA"]
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    """Solo las cuatro acciones (sin el INDICE)."""
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")[ACTIVOS]


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.pct_change().dropna()


def retorno_portafolio(retornos: pd.DataFrame, pesos: pd.Series) -> pd.Series:
    """Retorno diario del portafolio con pesos fijos: Σ wᵢ·rᵢ."""
    raise NotImplementedError("TODO")


def retorno_esperado(retornos: pd.DataFrame, pesos: pd.Series) -> float:
    """Retorno esperado anual: pesos · media diaria × 252."""
    raise NotImplementedError("TODO")


def volatilidad_portafolio(retornos: pd.DataFrame, pesos: pd.Series) -> float:
    """√(wᵀ Σ w) con Σ = covarianza diaria × 252."""
    raise NotImplementedError("TODO")


def beneficio_diversificacion(retornos: pd.DataFrame, pesos: pd.Series) -> float:
    """1 - vol del portafolio / promedio ponderado de las vol anuales individuales."""
    raise NotImplementedError("TODO")


def buy_and_hold(precios: pd.DataFrame, pesos: pd.Series, capital: float) -> tuple[pd.Series, pd.Series]:
    """Compra el primer día (capital × peso / precio inicial acciones de cada activo) y no
    vuelve a operar. Devuelve (valor diario del portafolio, pesos el último día).
    """
    raise NotImplementedError("TODO")


def rebalanceo_diario(precios: pd.DataFrame, pesos: pd.Series, capital: float) -> pd.Series:
    """Valor del portafolio rebalanceando todos los días: capital × Π(1 + retorno del portafolio).
    El índice arranca en la SEGUNDA fecha (la del primer retorno).
    """
    raise NotImplementedError("TODO")
