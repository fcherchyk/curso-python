"""Series de tiempo sobre precios.csv (columnas: fecha, ACME, BETA, CIRC, DELTA, INDICE)."""

from pathlib import Path

import pandas as pd


def cargar_precios(ruta: Path | str) -> pd.DataFrame:
    """DataFrame con la fecha como DatetimeIndex (llamado "fecha")."""
    raise NotImplementedError("TODO")


def cierres_mensuales(precios: pd.DataFrame) -> pd.DataFrame:
    """Último precio de cada mes (resample a fin de mes)."""
    raise NotImplementedError("TODO")


def retornos_mensuales(precios: pd.DataFrame) -> pd.DataFrame:
    """Retorno de cada mes a partir de los cierres mensuales, sin la primera fila NaN."""
    raise NotImplementedError("TODO")


def rendimiento_por_anio(precios: pd.DataFrame, columna: str) -> dict[int, float]:
    """Para cada año, (último precio del año / último precio del año ANTERIOR) - 1,
    redondeado a 4 decimales. El primer año se mide contra su PRIMER precio.
    """
    raise NotImplementedError("TODO")


def cruces_alcistas(precio: pd.Series, corta: int, larga: int) -> list[pd.Timestamp]:
    """Fechas en que la media móvil corta pasa a estar POR ENCIMA de la larga
    (hoy arriba y ayer no). Ignorá el período sin datos suficientes de la larga.
    """
    raise NotImplementedError("TODO")
