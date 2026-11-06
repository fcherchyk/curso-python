# Portfolios: weights, covariance and diversification

Hardly anyone invests in a single asset. A **portfolio** is a combination with **weights** (what
fraction of the capital goes to each asset), and it has an almost magical property: its risk is
**lower than the average** of the risks of its parts. In this chapter we use only the four stocks
(without INDEX).

## Weights and return

```python
assets = ["ACME", "BETA", "CIRC", "DELTA"]
weights = pd.Series(0.25, index=assets)     # equal parts; must add up to 1
r = prices[assets].pct_change().dropna()

r_port = r @ weights                        # the portfolio's daily return: Σ wᵢ·rᵢ
```

Since simple returns **aggregate across assets** (chapter 1), the portfolio's return is the
weighted average. The expected annual return is `weights @ r.mean() * 252` (0.1216 with equal
weights).

## Risk: the covariance matrix

The portfolio's volatility is **not** the weighted average of the volatilities. It depends on
how the assets move **relative to each other**:

```text
σ²_p = wᵀ Σ w = Σᵢ Σⱼ wᵢ wⱼ cov(i, j)
```

```python
annual_cov = r.cov() * 252
port_vol = np.sqrt(weights @ annual_cov @ weights)     # 0.1788
```

```
         ACME    BETA    CIRC   DELTA
ACME   0.0726  0.0223  0.0463  0.0103
BETA   0.0223  0.0309  0.0284  0.0066
CIRC   0.0463  0.0284  0.1460  0.0113
DELTA  0.0103  0.0066  0.0113  0.0115
```

The diagonal holds the variances (vol²) and the rest, the covariances. With `@`, the NumPy linear
algebra from module 11 does all the work.

## Diversification

| | annual volatility |
|---|---|
| weighted average of the 4 stocks | 0.2336 |
| equal-weight portfolio           | 0.1788 |

The portfolio has **23.5 % less risk** than the average of its parts, without giving up expected
return. It's the only "free lunch" in finance: it comes from correlations being below 1, so the
moves partly offset each other.

```python
benefit = 1 - port_vol / (weights @ individual_vol)
```

- With correlation 1 (everything moves the same way) there's no benefit.
- The lower the correlations, the bigger the benefit.
- There's a floor: **systematic risk** (market risk, which affects everyone) can't be
  diversified away. Only each company's **idiosyncratic** risk is eliminated.

## Buy & hold and weight drift

If you buy once and never touch anything (**buy & hold**), the weights **change on their own**:
whatever goes up weighs more and more.

```python
capital = 1000
shares = capital * weights / prices.iloc[0]          # how many shares of each I bought
value = (prices[assets] * shares).sum(axis=1)        # daily value: 1351.27 at the end
final_weights = prices.iloc[-1] * shares / value.iloc[-1]
```

```
ACME 0.261   BETA 0.164   CIRC 0.289   DELTA 0.285
```

BETA dropped to 16 % and CIRC rose to 29 %: the portfolio is **no longer** the one you chose,
and its risk has changed.

## Rebalancing

**Rebalancing** means selling what went up and buying what went down to get back to the target
weights. The extreme case is rebalancing **every day**, which is the same as applying fixed
weights to the returns:

```python
rebal_value = capital * (1 + r @ weights).cumprod()     # 1388.07 at the end
```

On this data, daily rebalancing came out ahead (1388 versus 1351), but that's not a rule: in
strongly trending markets buy & hold usually wins, and in choppy markets rebalancing "buys low
and sells high". In practice you rebalance monthly, quarterly, or when a weight drifts beyond a
threshold, because **every trade has costs** (we'll see this in backtesting).

## Summary

- Portfolio return: `r @ weights`. Expected annual return: `weights @ r.mean() * 252`.
- Volatility: `√(wᵀ Σ w)` with `Σ = r.cov() * 252`. It's not the average of the volatilities.
- Diversifying reduces idiosyncratic risk thanks to correlations below 1.
- With buy & hold the weights drift; rebalancing brings them back to target.

## Exercise

Compute a portfolio's return, expected return and volatility, the diversification benefit, the
buy & hold value with the final weights, and the value with daily rebalancing.

**Further reading:** H. Markowitz, *Portfolio Selection* (1952);
[Investopedia: Diversification](https://www.investopedia.com/terms/d/diversification.asp).
