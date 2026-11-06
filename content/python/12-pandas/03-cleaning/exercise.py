"""Data cleaning. Everything vectorized (.str, to_numeric), no loops or apply."""

import pandas as pd


def normalize_names(s: pd.Series) -> pd.Series:
    """No surrounding spaces, inner spaces collapsed to one, and in Title Case.

    "  alice   SMITH " → "Alice Smith". Nulls stay null.
    """
    raise NotImplementedError("TODO")


def parse_amounts(s: pd.Series) -> pd.Series:
    """"$ 1.234,50" → 1234.5 (float). Empty or invalid → NaN."""
    raise NotImplementedError("TODO")


def nulls_per_column(df: pd.DataFrame) -> dict[str, int]:
    """Number of nulls per column, only for columns that have any."""
    raise NotImplementedError("TODO")


def clean_customers(raw: pd.DataFrame) -> pd.DataFrame:
    """Full pipeline (don't modify `raw`):
    1. email: strip + lowercase; drop the rows without an email
    2. name: normalize_names
    3. age: numeric, invalid → null, dtype "Int64"
    4. balance: parse_amounts
    5. city: strip + Title Case; nulls → "Unknown"
    6. no duplicates by email (keep the first)
    7. index 0..n-1
    """
    raise NotImplementedError("TODO")
