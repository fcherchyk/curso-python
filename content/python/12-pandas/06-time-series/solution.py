from pathlib import Path

import pandas as pd


def load_prices(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path, index_col="date", parse_dates=True)


def monthly_closes(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.resample("ME").last()


def monthly_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return monthly_closes(prices).pct_change().dropna()


def yearly_performance(prices: pd.DataFrame, column: str) -> dict[int, float]:
    series = prices[column]
    closes = series.resample("YE").last()
    # Base: the previous year's close; for the first year, the first price.
    bases = closes.shift(1).fillna(series.iloc[0])
    perf = (closes / bases - 1).round(4)
    return {date.year: float(value) for date, value in perf.items()}


def bullish_crossovers(price: pd.Series, short: int, long: int) -> list[pd.Timestamp]:
    short_ma = price.rolling(short).mean()
    long_ma = price.rolling(long).mean()
    above = (short_ma > long_ma) & long_ma.notna()
    crossover = above & ~above.shift(1, fill_value=False)
    # The first day with a long average isn't a crossover: we don't know where it was before.
    crossover &= long_ma.shift(1).notna()
    return list(price.index[crossover])
