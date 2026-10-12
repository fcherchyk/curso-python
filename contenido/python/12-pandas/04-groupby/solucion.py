import pandas as pd


def total_por_sucursal(ventas: pd.DataFrame) -> pd.Series:
    return ventas.groupby("sucursal")["total"].sum().sort_values(ascending=False)


def resumen_por_categoria(ventas: pd.DataFrame) -> pd.DataFrame:
    resumen = ventas.groupby("categoria").agg(
        unidades=("cantidad", "sum"),
        facturacion=("total", "sum"),
        ticket_promedio=("total", "mean"),
        productos=("producto", "nunique"),
    )
    return resumen.assign(ticket_promedio=resumen["ticket_promedio"].round(2)).sort_values(
        "facturacion", ascending=False
    )


def participacion_en_sucursal(ventas: pd.DataFrame) -> pd.Series:
    return ventas["total"] / ventas.groupby("sucursal")["total"].transform("sum")


def tabla_sucursal_categoria(ventas: pd.DataFrame) -> pd.DataFrame:
    return pd.pivot_table(
        ventas, values="total", index="sucursal", columns="categoria", aggfunc="sum", fill_value=0
    )


def producto_top_por_sucursal(ventas: pd.DataFrame) -> dict[str, str]:
    unidades = ventas.groupby(["sucursal", "producto"])["cantidad"].sum()
    maximos = unidades.groupby(level="sucursal").idxmax()  # tuplas (sucursal, producto)
    return {sucursal: producto for sucursal, producto in maximos}
