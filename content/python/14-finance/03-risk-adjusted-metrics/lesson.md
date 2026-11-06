# Risk-adjusted metrics: Sharpe, Sortino, correlation and beta

CIRC returned 15 % a year and so did DELTA. Are they equally good? No: CIRC got there with
38 % volatility and a 51 % fall, and DELTA with 11 % volatility and a 12 % fall.
Risk-adjusted metrics answer the question: **how much return do I get for each unit of
risk?**

## The risk-free rate

First things first: investing in something risky only makes sense if it pays **more** than the
risk-free alternative (short-term US Treasury bills, for example). What matters is the
**excess return** over that rate. We use 4 % a year, which in daily terms is:

```python
daily_rf = 0.04 / 252
excess = returns - daily_rf
```

## Sharpe ratio

```text
Sharpe = mean(daily excess) / std(daily returns) × √252
```

It's the excess return per unit of volatility, annualized. The mean scales with 252 and the
standard deviation with √252, so the ratio scales with 252 / √252 = √252. By convention, Sharpe
uses the **arithmetic** mean of returns (unlike the compounded annualized return from
chapter 1).

```
ACME 0.40   BETA −0.36   CIRC 0.46   DELTA 0.98   INDEX 0.36
```

DELTA's Sharpe is almost twice CIRC's: the same return with much less risk. As a reference, a
Sharpe above 1 sustained over time is very good, and a negative one means you would have been
better off with the risk-free rate.

## Sortino ratio

Sharpe penalizes **upside** volatility just as much as downside volatility, but nobody minds
gains. Sortino only uses the **downside deviation**:

```python
downside = excess.clip(upper=0)                          # positive excess counts as 0
downside_dev = np.sqrt((downside ** 2).mean()) * np.sqrt(252)
sortino = excess.mean() * 252 / downside_dev
```

```
ACME 0.58   BETA −0.49   CIRC 0.69   DELTA 1.46   INDEX 0.52
```

Watch out: the downside deviation is computed over **all** days (with 0 on the positive ones),
not just over the negative ones.

## Correlation

```python
r.corr()
```

```
        ACME  BETA  CIRC  DELTA   INDEX
ACME    1.00  0.47  0.45   0.36    0.69
DELTA   0.36  0.35  0.28   1.00    0.45
```

It measures whether two assets **move together** (+1), in opposite directions (−1) or
independently (0). It's the key to diversification in the next chapter: combining
**weakly correlated** assets reduces the risk of the whole. DELTA is the asset least correlated
with the rest.

Careful: correlation **changes over time**, and it tends to rise in crises. Exactly when you
need it most, diversification works worst.

## Beta

Beta measures **how much an asset moves when the market moves**:

```text
β = cov(r_asset, r_market) / var(r_market)
```

```python
beta = r["ACME"].cov(r["INDEX"]) / r["INDEX"].var()     # 1.16
```

```
ACME 1.16   BETA 0.78   CIRC 1.46   DELTA 0.30
```

- β = 1: it moves just like the market. β > 1 amplifies (CIRC: if the index falls 10 %, it's
  expected to fall 14.6 %); β < 1 dampens.
- Beta is the slope of the regression of the asset's returns against the market's. It's the
  heart of the **CAPM**, which says the expected return depends only on market risk (beta),
  because the rest of the risk can be diversified away.
- What the asset returns above what its beta predicts is called **alpha**.

## Summary

- Work with the **excess** over the risk-free rate.
- Sharpe: `excess.mean() / r.std() * √252`. Sortino: the same, but dividing only by the
  downside deviation.
- `corr()` to see what moves together; low correlations are the ones that diversify.
- Beta = cov / market var: sensitivity to the market.

## Exercise

Implement Sharpe, Sortino, beta against the index, and a function that finds the asset least
correlated with a given one.

**Further reading:** W. Sharpe, *The Sharpe Ratio* (1994);
[Investopedia: Sortino Ratio](https://www.investopedia.com/terms/s/sortinoratio.asp).
