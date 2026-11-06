"""Time series on prices.csv (columns: date, ACME, BETA, CIRC, DELTA, INDEX)."""

from pathlib import Path

import pandas as pd


def load_prices(path: Path | str) -> pd.DataFrame:
    """DataFrame with the date as a DatetimeIndex (named "date")."""
    raise NotImplementedError("TODO")


def monthly_closes(prices: pd.DataFrame) -> pd.DataFrame:
    """Last price of each month (resample to month end)."""
    raise NotImplementedError("TODO")


def monthly_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Return of each month based on the monthly closes, without the first NaN row."""
    raise NotImplementedError("TODO")


def yearly_performance(prices: pd.DataFrame, column: str) -> dict[int, float]:
    """For each year, (last price of the year / last price of the PREVIOUS year) - 1,
    rounded to 4 decimals. The first year is measured against its FIRST price.
    """
    raise NotImplementedError("TODO")


def bullish_crossovers(price: pd.Series, short: int, long: int) -> list[pd.Timestamp]:
    """Dates on which the short moving average moves ABOVE the long one
    (above today and not yesterday). Ignore the period without enough data for the long one.
    """
    raise NotImplementedError("TODO")
