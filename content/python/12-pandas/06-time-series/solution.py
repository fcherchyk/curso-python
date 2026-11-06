from pathlib import Path

import pandas as pd


def cargar_precios(ruta: Path | str) -> pd.DataFrame:
    return pd.read_csv(ruta, index_col="fecha", parse_dates=True)


def cierres_mensuales(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.resample("ME").last()


def retornos_mensuales(precios: pd.DataFrame) -> pd.DataFrame:
    return cierres_mensuales(precios).pct_change().dropna()


def rendimiento_por_anio(precios: pd.DataFrame, columna: str) -> dict[int, float]:
    serie = precios[columna]
    cierres = serie.resample("YE").last()
    # Base: el cierre del año anterior; para el primer año, el primer precio.
    bases = cierres.shift(1).fillna(serie.iloc[0])
    rend = (cierres / bases - 1).round(4)
    return {fecha.year: float(valor) for fecha, valor in rend.items()}


def cruces_alcistas(precio: pd.Series, corta: int, larga: int) -> list[pd.Timestamp]:
    media_corta = precio.rolling(corta).mean()
    media_larga = precio.rolling(larga).mean()
    arriba = (media_corta > media_larga) & media_larga.notna()
    cruce = arriba & ~arriba.shift(1, fill_value=False)
    # El primer día con media larga no es un cruce: no sabemos dónde estaba antes.
    cruce &= media_larga.shift(1).notna()
    return list(precio.index[cruce])
