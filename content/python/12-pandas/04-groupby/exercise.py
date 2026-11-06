"""groupby: grouping and aggregating.

`sales` has index "id" and the columns date, branch, product, quantity, category,
unit_price and total (= quantity * unit_price).
"""

import pandas as pd


def total_by_branch(sales: pd.DataFrame) -> pd.Series:
    """Revenue (sum of total) per branch, from highest to lowest."""
    raise NotImplementedError("TODO")


def category_summary(sales: pd.DataFrame) -> pd.DataFrame:
    """Per category, with named aggregations:
    units (sum of quantity), revenue (sum of total), average_ticket (mean of total,
    rounded to 2) and products (number of distinct products).
    Sorted by revenue descending.
    """
    raise NotImplementedError("TODO")


def share_of_branch(sales: pd.DataFrame) -> pd.Series:
    """For each sale, total / revenue of ITS branch (transform). Same index as sales."""
    raise NotImplementedError("TODO")


def branch_category_table(sales: pd.DataFrame) -> pd.DataFrame:
    """Pivot table: rows = branch, columns = category, cells = sum of total, 0 if none."""
    raise NotImplementedError("TODO")


def top_product_by_branch(sales: pd.DataFrame) -> dict[str, str]:
    """For each branch, the product with the most UNITS sold."""
    raise NotImplementedError("TODO")
