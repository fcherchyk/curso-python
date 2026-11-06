import pandas as pd


def enrich(sales: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    r = sales.merge(products, on="product", how="left", validate="many_to_one")
    return r.assign(total=r["quantity"] * r["unit_price"])


def products_not_in_catalog(sales: pd.DataFrame, products: pd.DataFrame) -> list[str]:
    r = sales.merge(products, on="product", how="left", indicator=True)
    return sorted(r.loc[r["_merge"] == "left_only", "product"].unique().tolist())


def revenue_by_category(sales: pd.DataFrame, products: pd.DataFrame) -> dict[str, float]:
    r = sales.merge(products, on="product", how="inner", validate="many_to_one")
    totals = (r["quantity"] * r["unit_price"]).groupby(r["category"]).sum()
    return totals.to_dict()


def stack(parts: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return (
        pd.concat(parts, names=["batch", None])
        .reset_index(level="batch")
        .reset_index(drop=True)
    )
