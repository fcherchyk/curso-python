from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

CSV = Path(__file__).parent / "precios.csv"


def cargar(activo: str) -> pd.Series:
    return pd.read_csv(CSV, parse_dates=["fecha"], index_col="fecha")[activo]


def senal_cruce(precios: pd.Series, corta: int = 20, larga: int = 50) -> pd.Series:
    return (precios.rolling(corta).mean() > precios.rolling(larga).mean()).astype(int)


def posicion(senal: pd.Series) -> pd.Series:
    return senal.shift(1).fillna(0)


def _operaciones(pos: pd.Series) -> pd.Series:
    return pos.diff().fillna(pos).abs()


def retornos_estrategia(precios: pd.Series, pos: pd.Series, costo: float = 0.001) -> pd.Series:
    r = precios.pct_change().fillna(0)
    return pos * r - costo * _operaciones(pos)


def resumen(precios: pd.Series, corta: int = 20, larga: int = 50, costo: float = 0.001) -> dict:
    pos = posicion(senal_cruce(precios, corta, larga))
    r_estrategia = retornos_estrategia(precios, pos, costo)
    return {
        "estrategia": float((1 + r_estrategia).prod() - 1),
        "buy_and_hold": float(precios.iloc[-1] / precios.iloc[0] - 1),
        "operaciones": int(_operaciones(pos).sum()),
        "exposicion": float(pos.mean()),
    }


def grafico_equity(precios: pd.Series, capital: float = 1000, corta: int = 20, larga: int = 50,
                   costo: float = 0.001) -> Figure:
    pos = posicion(senal_cruce(precios, corta, larga))
    r = precios.pct_change().fillna(0)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(capital * (1 + retornos_estrategia(precios, pos, costo)).cumprod(), label="Estrategia")
    ax.plot(capital * (1 + r).cumprod(), label="Buy & hold", alpha=0.7)
    ax.set(ylabel="Capital ($)", title=f"Cruce de medias {corta}/{larga} vs buy & hold")
    ax.legend()
    return fig
