# Prices and returns

In finance you almost never work with prices directly, but with **returns**: how much the
price changed, proportionally. A price of 100 versus one of 50 tells you nothing. Knowing that
both went up 2 % yesterday does let you compare them. This chapter lays the groundwork for the whole module.

## The data

Every chapter ships `prices.csv`: **synthetic** daily closing prices for four made-up stocks
(`ACME`, `BETA`, `CIRC`, `DELTA`) and a market index (`INDEX`), from 2023 to 2025. They are
synthetic so the tests are reproducible and don't depend on the internet. With real data the
code is identical:

```python
import yfinance as yf                                        # pip install yfinance
prices = yf.download(["AAPL", "MSFT", "SPY"], start="2023-01-01")["Close"]
```

```python
prices = pd.read_csv("prices.csv", parse_dates=["date"], index_col="date")
prices.shape          # (783, 5): ~252 trading days per year
```

There are only **trading days**: a market year has about **252** sessions. That number shows up
every time you annualize something.

## Simple return

```text
r_t = P_t / P_{t-1} - 1
```

```python
returns = prices.pct_change().dropna()   # the first day has no previous day: NaN
```

```
              ACME    BETA    CIRC   DELTA   INDEX
date
2023-01-03  0.0225  0.0248  0.0263  0.0078  0.0170
2023-01-04  0.0179  0.0145  0.0052  0.0037  0.0119
```

Properties:

- **They aggregate across assets**: a portfolio's return is the weighted average of the simple
  returns of its assets (we'll use this in the portfolios chapter).
- **They don't add up over time**: +10 % followed by −10 % is not 0 but 1.1 × 0.9 − 1 = −1 %.
  They **compound**: the cumulative return is the product.

```python
cumulative = (1 + returns).prod() - 1      # ACME: 0.4118 → +41.18 % over the whole period
curve = (1 + returns).cumprod()            # growth of $1 invested
```

## Log return

```text
l_t = ln(P_t / P_{t-1}) = ln(1 + r_t)
```

```python
log_ret = np.log(prices / prices.shift(1)).dropna()
```

- **They add up over time**: the log return of the whole period is the sum of the daily ones.
  `log_ret.sum()` for ACME gives 0.3449, and `np.exp(0.3449) - 1` gives 0.4118, the same cumulative return.
- For small changes, `l ≈ r`. With large changes they diverge.
- **They don't aggregate across assets**: a portfolio's log return is not the average of the
  log returns.

Rule of thumb: **simple for portfolios** and **log for adding over time or for statistical
models**.

## Annualizing

A 41 % total return over three years can't be compared directly with a 15 % return over one.
You have to bring them to a common basis, the **year**:

```text
R_annual = (1 + R_total) ^ (252 / n) - 1
```

where `n` is the number of daily returns. It's compound interest in reverse.

```python
annual = (1 + returns).prod() ** (252 / len(returns)) - 1    # ACME: 0.1175
```

Do **not** multiply the average daily return by 252: it ignores compounding and overestimates
when there is volatility.

## CAGR

The **compound annual growth rate** is the same idea, but measured with calendar dates instead
of counting sessions:

```text
CAGR = (P_final / P_initial) ^ (1 / years) - 1
```

```python
years = (prices.index[-1] - prices.index[0]).days / 365.25
cagr = (prices.iloc[-1] / prices.iloc[0]) ** (1 / years) - 1   # ACME: 0.122
```

The difference from the previous figure (0.1175 versus 0.122) comes from the CSV starting with
the January 2 price, without that day's return, and from the day-count convention. In practice,
pick one convention and use it consistently.

## Summary

- `pct_change()` for simple returns and `np.log(p / p.shift())` for log returns; `dropna()`.
- Simple: weighted across assets and compounded over time (`(1 + r).prod() - 1`).
- Log: added over time; `exp(sum) - 1` gets you back to the simple return.
- Annualize by compounding: `(1 + R)^(252/n) - 1`; CAGR with calendar dates.

## Exercise

Compute simple and log returns, the cumulative return, the annualized return and the CAGR.

**Further reading:** *Python for Finance* (Yves Hilpisch), chapter "Financial Time Series";
[pandas: pct_change](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html).
