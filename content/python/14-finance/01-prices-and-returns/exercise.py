"""Precios y retornos. `precios` es un DataFrame con índice de fechas y una columna por activo."""

from pathlib import Path

import numpy as np  # noqa: F401
import pandas as pd

CSV = Path(__file__).parent / "precios.csv"
DIAS_HABILES = 252


def cargar() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")


def retornos_simples(precios: pd.DataFrame) -> pd.DataFrame:
    """P_t / P_{t-1} - 1, sin la primera fila (NaN)."""
    raise NotImplementedError("TODO")


def retornos_log(precios: pd.DataFrame) -> pd.DataFrame:
    """ln(P_t / P_{t-1}), sin la primera fila."""
    raise NotImplementedError("TODO")


def retorno_acumulado(retornos: pd.DataFrame) -> pd.Series:
    """Retorno total del período por activo, componiendo los retornos simples."""
    raise NotImplementedError("TODO")


def retorno_anualizado(retornos: pd.DataFrame) -> pd.Series:
    """(1 + acumulado) ** (252 / cantidad de retornos) - 1, por activo."""
    raise NotImplementedError("TODO")


def cagr(precios: pd.DataFrame) -> pd.Series:
    """(último / primero) ** (1 / años) - 1, con años = días de calendario / 365.25."""
    raise NotImplementedError("TODO")
