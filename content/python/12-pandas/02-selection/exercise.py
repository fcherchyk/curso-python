"""Selecting and filtering.

`sales` is the DataFrame from sales.csv with index "id", "date" parsed and the column
"total" = quantity * unit_price (as in the previous chapter; the tests build it).
"""

import pandas as pd


def large_sales_at(sales: pd.DataFrame, branch: str, minimum: float) -> pd.DataFrame:
    """Sales from that branch with total >= minimum, only the product and total columns,
    sorted by total descending.
    """
    raise NotImplementedError("TODO")


def for_products(sales: pd.DataFrame, products: list[str]) -> pd.Series:
    """Quantities (column "quantity") of the sales of those products (isin)."""
    raise NotImplementedError("TODO")


def lookup(sales: pd.DataFrame, category: str, min_quantity: int) -> list[int]:
    """Ids of the sales in that category with quantity >= min_quantity, using df.query
    with variables (@). Sorted.
    """
    raise NotImplementedError("TODO")


def top_and_first_label(sales: pd.DataFrame) -> tuple[int, int]:
    """Sort by total descending and return (id of the FIRST row in that order, quantity of
    the sale whose id is the SMALLEST). Use iloc and loc respectively.
    """
    raise NotImplementedError("TODO")


def with_discount(sales: pd.DataFrame, category: str, pct: float) -> pd.DataFrame:
    """A NEW DataFrame with unit_price and total reduced by `pct` (0.1 = 10 %) for the
    sales in that category. Do NOT modify `sales`.
    """
    raise NotImplementedError("TODO")
