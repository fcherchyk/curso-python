import pandas as pd


def ventas_grandes_de(ventas: pd.DataFrame, sucursal: str, minimo: float) -> pd.DataFrame:
    mascara = (ventas["sucursal"] == sucursal) & (ventas["total"] >= minimo)
    return ventas.loc[mascara, ["producto", "total"]].sort_values("total", ascending=False)


def de_productos(ventas: pd.DataFrame, productos: list[str]) -> pd.Series:
    return ventas.loc[ventas["producto"].isin(productos), "cantidad"]


def consulta(ventas: pd.DataFrame, categoria: str, minima_cantidad: int) -> list[int]:
    resultado = ventas.query("categoria == @categoria and cantidad >= @minima_cantidad")
    return sorted(resultado.index.tolist())


def top_y_primera_etiqueta(ventas: pd.DataFrame) -> tuple[int, int]:
    ordenado = ventas.sort_values("total", ascending=False)
    return int(ordenado.index[0]), int(ordenado.loc[ventas.index.min(), "cantidad"])


def con_descuento(ventas: pd.DataFrame, categoria: str, pct: float) -> pd.DataFrame:
    resultado = ventas.copy()
    mascara = resultado["categoria"] == categoria
    resultado["precio_unitario"] = resultado["precio_unitario"].astype(float)
    resultado["total"] = resultado["total"].astype(float)
    resultado.loc[mascara, ["precio_unitario", "total"]] *= 1 - pct
    return resultado
