# Risk: volatility, drawdown and VaR

A high return means nothing without the risk you had to take to get it. "Risk" is not a single
thing, and each measure answers a different question:

| Question                                            | Measure                |
|-----------------------------------------------------|------------------------|
| How much does it swing in a typical year?            | annualized volatility  |
| What was the worst fall from a peak?                  | maximum drawdown       |
| How much can I lose on a bad day (with 95 % confidence)? | VaR                 |
| And on the days beyond the VaR, how much do I lose on average? | CVaR / Expected Shortfall |

We use the daily simple returns from the previous chapter: `r = prices.pct_change().dropna()`.

## Volatility

It's the **standard deviation of returns**. It measures how far they stray from the average,
both up and down.

```python
daily_vol = r.std()
annual_vol = r.std() * np.sqrt(252)
```

```
ACME 0.269   BETA 0.176   CIRC 0.382   DELTA 0.107   INDEX 0.160
```

Why `√252` and not `252`? If daily returns are independent, the **variances** add up: the annual
variance is 252 times the daily one, and the standard deviation is its square root. This is the
"square-root-of-time rule". With 16 % annual volatility, INDEX typically moves ±1 % per day
(0.16 / √252 ≈ 0.010).

Limitations: it penalizes gains and losses equally, and it assumes something close to a normal
distribution. Real markets have **fat tails**: extreme days are far more frequent than the
normal distribution predicts.

## Drawdown

The **drawdown** is how far you are below the **previous peak**. It's the measure closest to what
an investor feels ("how much have I lost since the top?").

```python
peak = prices.cummax()                   # running maximum up to each date
drawdown = prices / peak - 1             # 0 at peaks, negative during falls
max_dd = drawdown.min()                  # CIRC: −0.51
```

CIRC was at one point **51 % below** its peak (from 2023-09-06 to 2024-06-17). To recover from a
51 % fall you need to **rise 104 %**: 1 / (1 − 0.51) − 1. That's why large falls are so damaging,
and why drawdown matters more than volatility to many investors.

## Historical VaR

The 95 % **Value at Risk** answers: *"on 95 out of 100 days, the loss doesn't exceed X"*. The
**historical** version assumes no distribution: it takes the 5th percentile of the observed
returns.

```python
var_95 = -r.quantile(0.05)       # ACME: 0.0284 → on the worst 5 % of days it loses ≥ 2.84 %
```

It's usually expressed as a **positive** loss, hence the minus sign. With a $100,000 position in
ACME, the 95 % daily VaR is about $2,840.

The VaR **doesn't tell you how much you lose in that 5 %**: it could be 3 % or 30 %. That's what
CVaR is for.

## CVaR (Expected Shortfall)

The average of the returns **on the days beyond the VaR**:

```python
q = r.quantile(0.05)
cvar_95 = -r[r <= q].mean()      # ACME: 0.0345
```

It's always greater than or equal to the VaR and describes the tail better. Banking regulators
(Basel) moved from VaR to Expected Shortfall precisely for that reason.

## Summary

- Volatility: `r.std() * √252`. Measures symmetric swings and assumes normal tails.
- Drawdown: `p / p.cummax() - 1`; the maximum drawdown is its minimum. A 50 % fall requires
  +100 % to recover.
- Historical VaR: `-r.quantile(1 - level)`, the loss not exceeded on `level` % of days.
- CVaR: the average loss on the days beyond the VaR.
- **It's all historical**: past risk doesn't guarantee the future.

## Exercise

Implement annualized volatility, the drawdown series, maximum drawdown, and historical VaR and
CVaR.

**Further reading:** [Investopedia: Value at Risk](https://www.investopedia.com/terms/v/var.asp),
*Fooled by Randomness* (N. N. Taleb) on fat tails.
