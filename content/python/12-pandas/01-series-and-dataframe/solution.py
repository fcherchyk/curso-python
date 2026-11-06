from pathlib import Path

import pandas as pd


def price_series(prices: dict[str, float]) -> pd.Series:
    return pd.Series(prices, name="price").sort_index()


def from_records(records: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(records, columns=["product", "price", "stock"])


def load_sales(path: Path | str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col="id", parse_dates=["date"])
    df["total"] = df["quantity"] * df["unit_price"]
    return df


def summary(sales: pd.DataFrame) -> dict[str, object]:
    return {
        "rows": len(sales),
        "total": int(sales["total"].sum()),
        "average_ticket": round(float(sales["total"].mean()), 2),
        "largest_sale": int(sales["total"].idxmax()),
        "most_frequent_branch": sales["branch"].value_counts().idxmax(),
    }
