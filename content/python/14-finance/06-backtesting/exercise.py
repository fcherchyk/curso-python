"""Backtesting de un cruce de medias móviles sobre un solo activo (una Series de precios)."""

from pathlib import Path

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "precios.csv"


def cargar(activo: str) -> pd.Series:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")[activo]


def senal_cruce(precios: pd.Series, corta: int = 20, larga: int = 50) -> pd.Series:
    """1 si la media móvil corta > la larga, 0 si no (incluidos los días sin datos suficientes).
    dtype int.
    """
    raise NotImplementedError("TODO")


def posicion(senal: pd.Series) -> pd.Series:
    """La posición de cada día es la señal del día ANTERIOR (sin look-ahead). El primer día, 0."""
    raise NotImplementedError("TODO")


def retornos_estrategia(precios: pd.Series, pos: pd.Series, costo: float = 0.001) -> pd.Series:
    """pos × retorno diario (pct_change con el primer día en 0)
    - costo × |cambio de posición| (el cambio del primer día es la posición misma).
    """
    raise NotImplementedError("TODO")


def resumen(precios: pd.Series, corta: int = 20, larga: int = 50, costo: float = 0.001) -> dict:
    """{"estrategia": retorno total, "buy_and_hold": retorno total,
        "operaciones": cantidad de cambios de posición (int), "exposicion": fracción de días comprado}
    """
    raise NotImplementedError("TODO")


def grafico_equity(precios: pd.Series, capital: float = 1000, corta: int = 20, larga: int = 50,
                   costo: float = 0.001) -> Figure:
    """Dos líneas: capital × Π(1 + r_estrategia) con label "Estrategia" y
    capital × Π(1 + r) con label "Buy & hold". Leyenda e ylabel "Capital ($)".
    """
    raise NotImplementedError("TODO")
