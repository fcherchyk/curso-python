import pandas as pd


def enriquecer(ventas: pd.DataFrame, productos: pd.DataFrame) -> pd.DataFrame:
    r = ventas.merge(productos, on="producto", how="left", validate="many_to_one")
    return r.assign(total=r["cantidad"] * r["precio_unitario"])


def productos_fuera_de_catalogo(ventas: pd.DataFrame, productos: pd.DataFrame) -> list[str]:
    r = ventas.merge(productos, on="producto", how="left", indicator=True)
    return sorted(r.loc[r["_merge"] == "left_only", "producto"].unique().tolist())


def facturacion_por_categoria(ventas: pd.DataFrame, productos: pd.DataFrame) -> dict[str, float]:
    r = ventas.merge(productos, on="producto", how="inner", validate="many_to_one")
    totales = (r["cantidad"] * r["precio_unitario"]).groupby(r["categoria"]).sum()
    return totales.to_dict()


def apilar(partes: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return (
        pd.concat(partes, names=["lote", None])
        .reset_index(level="lote")
        .reset_index(drop=True)
    )
