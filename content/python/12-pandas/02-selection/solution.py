import pandas as pd


def large_sales_at(sales: pd.DataFrame, branch: str, minimum: float) -> pd.DataFrame:
    mask = (sales["branch"] == branch) & (sales["total"] >= minimum)
    return sales.loc[mask, ["product", "total"]].sort_values("total", ascending=False)


def for_products(sales: pd.DataFrame, products: list[str]) -> pd.Series:
    return sales.loc[sales["product"].isin(products), "quantity"]


def lookup(sales: pd.DataFrame, category: str, min_quantity: int) -> list[int]:
    result = sales.query("category == @category and quantity >= @min_quantity")
    return sorted(result.index.tolist())


def top_and_first_label(sales: pd.DataFrame) -> tuple[int, int]:
    ordered = sales.sort_values("total", ascending=False)
    return int(ordered.index[0]), int(ordered.loc[sales.index.min(), "quantity"])


def with_discount(sales: pd.DataFrame, category: str, pct: float) -> pd.DataFrame:
    result = sales.copy()
    mask = result["category"] == category
    result["unit_price"] = result["unit_price"].astype(float)
    result["total"] = result["total"].astype(float)
    result.loc[mask, ["unit_price", "total"]] *= 1 - pct
    return result
