# Time series

Prices, daily sales, server metrics, sensors: a lot of data has a **date** as its main axis.
pandas was born at an investment fund precisely for this, and it has first-class tools for time
series: a date index you can slice by period, frequency changes (`resample`), rolling windows
(`rolling`), shifts (`shift`) and changes (`pct_change`). It's the foundation of the finance
module.

## The `DatetimeIndex`

```python
prices = pd.read_csv("prices.csv", index_col="date", parse_dates=True)
prices.index             # DatetimeIndex(['2023-01-02', ...], dtype='datetime64[ns]')
prices.index.min(), prices.index.max()
```

With a date index, slicing feels very natural:

```python
prices.loc["2024"]                        # all of 2024
prices.loc["2024-03"]                     # March 2024
prices.loc["2024-03-01":"2024-06-30"]     # a range (inclusive)
prices.loc[prices.index.dayofweek == 0]   # Mondays only
```

Useful attributes: `.year`, `.month`, `.day`, `.dayofweek`, `.quarter` and `.is_month_end` (on a
date column you access them through `.dt`, for example `df["date"].dt.month`).

## Changing the frequency: `resample`

`resample` is a `groupby` over time periods:

```python
prices.resample("ME").last()         # the last price of each month (ME = month end)
prices.resample("W").mean()          # weekly average
sales.resample("D").sum()            # daily total
prices.resample("YE").agg(["first", "last", "max"])
```

Common frequencies: `"D"` (day), `"B"` (business day), `"W"` (week), `"ME"` (month end), `"QE"`
(quarter end) and `"YE"` (year end). For closing prices, the representative value of the period
is the **last** one (`last()`), not the average.

## Shifting: `shift`

```python
prices["ACME"].shift(1)         # the PREVIOUS day's value, aligned with today
prices["ACME"].shift(-1)        # the next day's (careful: that's looking into the future!)
```

`shift` moves the data and keeps the index: each date ends up holding the previous date's value.
It's the tool for comparing with "yesterday" and, in finance, for **avoiding information that
didn't exist yet** (*look-ahead bias*, which we'll see in backtesting).

## Changes: `pct_change` and `diff`

```python
prices.pct_change()             # (today / yesterday) - 1  ← daily returns
prices.diff()                   # today - yesterday
prices.pct_change(periods=5)    # versus 5 days ago
(1 + returns).cumprod()         # cumulative return: growth of 1 dollar invested
```

`pct_change()` is exactly `prices / prices.shift(1) - 1`. The first row is `NaN` because there's
no previous day; drop it with `.dropna()`.

## Rolling windows: `rolling`

```python
prices["ACME"].rolling(20).mean()       # 20-day moving average
returns.rolling(60).std()               # rolling volatility
prices.rolling("30D").max()             # window by TIME (30 calendar days)
prices.expanding().max()                # all-time high up to each date
```

The first `window - 1` rows are `NaN`, because there isn't enough data yet (you can change that
with `min_periods`). `expanding()` is a window that keeps growing: useful for "highest so far" or
drawdowns.

## Combining tools: moving average crossovers

"On which days did the short average cross **above** the long one?"

```python
short = price.rolling(20).mean()
long = price.rolling(50).mean()
above = short > long
crossover = above & ~above.shift(1, fill_value=False)   # above today and not yesterday
price.index[crossover]
```

Comparing a condition with its own `shift` detects **state changes**. It's a pattern you'll reuse
a lot.

## Time zones

```python
idx.tz_localize("UTC").tz_convert("America/New_York")
```

Same as with `datetime`: store in UTC and convert for display.

## Summary

- `read_csv(..., index_col="date", parse_dates=True)` gives you a `DatetimeIndex`;
  `loc["2024-03"]` slices by period.
- `resample("ME").last()` and friends to change the frequency.
- `shift` to compare with the past; `pct_change`/`diff` for changes; `cumprod` to accumulate.
- `rolling(n)` for rolling windows; `expanding()` for all-time cumulative values.
- Condition + `shift` to detect state changes (crossovers).

## Exercise

On `prices.csv` (daily prices for ACME, BETA, CIRC, DELTA and an INDEX, from 2023 to 2025):
monthly closes, returns, moving averages, yearly performance and the bullish moving average
crossovers.

**Further reading:** [Time series / date functionality](https://pandas.pydata.org/docs/user_guide/timeseries.html),
[Windowing operations](https://pandas.pydata.org/docs/user_guide/window.html).
