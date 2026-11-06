"""Series and DataFrame."""

from pathlib import Path

import pandas as pd


def price_series(prices: dict[str, float]) -> pd.Series:
    """Series with the prices, named "price", with the index sorted alphabetically."""
    raise NotImplementedError("TODO")


def from_records(records: list[dict[str, object]]) -> pd.DataFrame:
    """DataFrame with the columns in this order: product, price, stock."""
    raise NotImplementedError("TODO")


def load_sales(path: Path | str) -> pd.DataFrame:
    """Read sales.csv with:
    - the "id" column as the index
    - "date" as datetime
    - a new column "total" = quantity * unit_price
    """
    raise NotImplementedError("TODO")


def summary(sales: pd.DataFrame) -> dict[str, object]:
    """From what load_sales returns:
    {"rows": number of sales,
     "total": sum of "total",
     "average_ticket": mean of "total" rounded to 2 decimals,
     "largest_sale": id (index) of the sale with the largest total,
     "most_frequent_branch": the branch with the most sales (value_counts)}
    """
    raise NotImplementedError("TODO")
