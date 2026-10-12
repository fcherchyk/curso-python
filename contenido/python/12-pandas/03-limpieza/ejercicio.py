"""Limpieza de datos. Todo vectorizado (.str, to_numeric), sin bucles ni apply."""

import pandas as pd


def normalizar_nombres(s: pd.Series) -> pd.Series:
    """Sin espacios alrededor, espacios internos colapsados a uno y en Title Case.

    "  ana   PÉREZ " → "Ana Pérez". Los nulos siguen siendo nulos.
    """
    raise NotImplementedError("TODO")


def convertir_montos(s: pd.Series) -> pd.Series:
    """"$ 1.234,50" → 1234.5 (float). Vacíos o inválidos → NaN."""
    raise NotImplementedError("TODO")


def nulos_por_columna(df: pd.DataFrame) -> dict[str, int]:
    """Cantidad de nulos por columna, solo las columnas que tienen alguno."""
    raise NotImplementedError("TODO")


def limpiar_clientes(crudo: pd.DataFrame) -> pd.DataFrame:
    """Pipeline completo (no modifiques `crudo`):
    1. email: strip + minúsculas; descartá las filas sin email
    2. nombre: normalizar_nombres
    3. edad: numérica, inválidas → nulo, dtype "Int64"
    4. saldo: convertir_montos
    5. ciudad: strip + Title Case; nulos → "Desconocida"
    6. sin duplicados por email (quedate con el primero)
    7. índice 0..n-1
    """
    raise NotImplementedError("TODO")
