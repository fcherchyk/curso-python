from pathlib import Path

import pandas as pd


def serie_precios(precios: dict[str, float]) -> pd.Series:
    return pd.Series(precios, name="precio").sort_index()


def desde_registros(registros: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(registros, columns=["producto", "precio", "stock"])


def cargar_ventas(ruta: Path | str) -> pd.DataFrame:
    df = pd.read_csv(ruta, index_col="id", parse_dates=["fecha"])
    df["total"] = df["cantidad"] * df["precio_unitario"]
    return df


def resumen(ventas: pd.DataFrame) -> dict[str, object]:
    return {
        "filas": len(ventas),
        "total": int(ventas["total"].sum()),
        "ticket_promedio": round(float(ventas["total"].mean()), 2),
        "venta_mayor": int(ventas["total"].idxmax()),
        "sucursal_mas_frecuente": ventas["sucursal"].value_counts().idxmax(),
    }
