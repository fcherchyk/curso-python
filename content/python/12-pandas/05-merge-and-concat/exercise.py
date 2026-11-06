"""Combining tables: merge, join and concat."""

import pandas as pd


def enrich(sales: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Add the category and unit_price from the catalog to each sale, WITHOUT losing sales
    (sales of products outside the catalog end up with nulls). Validate that the relationship
    is many-to-one (if the catalog has repeated products, it must raise MergeError).
    Also add "total" = quantity * unit_price.
    """
    raise NotImplementedError("TODO")


def products_not_in_catalog(sales: pd.DataFrame, products: pd.DataFrame) -> list[str]:
    """Products sold that aren't in the catalog, without repeats and sorted (indicator=True)."""
    raise NotImplementedError("TODO")


def revenue_by_category(sales: pd.DataFrame, products: pd.DataFrame) -> dict[str, float]:
    """Sum of total per category, only for sales whose product is in the catalog (inner)."""
    raise NotImplementedError("TODO")


def stack(parts: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Concatenate the DataFrames one below the other, with a "batch" column (the dict key)
    as the FIRST column and an index 0..n-1.
    """
    raise NotImplementedError("TODO")
