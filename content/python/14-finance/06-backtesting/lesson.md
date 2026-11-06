# Backtesting: testing a strategy without fooling yourself

A **backtest** simulates how an investment rule would have done on historical data. It's easy to
code and **even easier to get wrong**: a buggy backtest always looks excellent. This chapter
builds a simple one and, above all, shows the traps.

## The strategy: moving-average crossover

A classic trend-following rule:

- **Short average** (20 days) above the **long average** (50 days): uptrend, **long** (invested).
- Otherwise: **out** (in cash).

```python
s = prices["ACME"]
short = s.rolling(20).mean()
long = s.rolling(50).mean()
signal = (short > long).astype(int)      # 1 = invested, 0 = out
```

For the first 49 days the long average is NaN, and `NaN > x` is `False`: the signal is 0 (out)
until there's enough data.

## Trap number one: *look-ahead bias*

The signal for day `t` uses day `t`'s **closing** price. You only know it once the day is over,
so **you can't have traded during that day with that information**. The position you actually
hold on day `t` is **yesterday's** signal:

```python
position = signal.shift(1).fillna(0)     # you trade the day after the signal
r = s.pct_change().fillna(0)
r_strategy = position * r
```

To see how badly forgetting the `shift` misleads you, try an absurd rule: "be invested on the
days it goes up".

```python
cheat = (r > 0) * r                      # no shift: it knows the future
honest = (r > 0).shift(1).fillna(False) * r
```

On ACME, the cheating version multiplies the capital **214 times** in three years, and the honest
one gains 8 %. With moving averages the error is less obvious (58 % versus 56 %), and that's why
it's so dangerous: the result looks believable.

## Transaction costs

Every time the position changes, you pay commissions and the *spread* (the difference between
the buy and sell price). A simple model charges a percentage on each change:

```python
trades = position.diff().fillna(position).abs()   # 1 on every entry or exit
r_net = position * r - 0.001 * trades             # 0.1 % per trade
```

`fillna(position)` counts the first entry if the position starts at 1. A strategy that trades a
lot can go from winner to loser on costs alone.

## Compare against buy & hold

A strategy is only worth it if it beats the simplest alternative: **buy and do nothing**.

| ACME (2023–2025) | total return | trades | time invested |
|---|---|---|---|
| Buy & hold                          | 41.2 % | 1  | 100 % |
| 20/50 crossover, no costs           | 55.6 % | 15 | 54 % |
| 20/50 crossover, 0.1 % per trade    | 53.3 % | 15 | 54 % |

On ACME the strategy won. On INDEX, the same rule returns **22 %** against **30 %** for buy &
hold: **it lost**. A result on a single asset over a single period proves nothing.

## The equity curve

```python
equity = capital * (1 + r_net).cumprod()
buy_hold = capital * (1 + r).cumprod()
fig, ax = plt.subplots()
ax.plot(equity, label="Strategy")
ax.plot(buy_hold, label="Buy & hold")
```

Look at the whole curve, not just the final number: when did it make money? How long was it
below its peak (drawdown, chapter 2)?

## Other traps

- **Overfitting**: trying 100 combinations of averages and keeping the best one finds noise, not
  a signal. Split the data: optimize on one period and validate on another you haven't looked
  at (*out-of-sample*).
- **Survivorship bias**: if you only test with companies that exist today, you skip the ones
  that went bankrupt.
- **Unrealistic execution**: assuming you trade exactly at the close, with no price impact.
- **Synthetic data**: these prices are a random walk. By construction, **no** strategy has a
  real edge on them; any "profit" is luck. The same can happen to you with real data without
  noticing.

Tools like `vectorbt` or `backtrader` handle the mechanics, but not these biases: those are
always on you.

## Summary

- Signal with data up to `t` → position at `t + 1`: `signal.shift(1)`. Without the shift, the
  backtest cheats.
- Strategy return: `position * r - cost * |Δposition|`.
- Always compare against buy & hold, across several assets and periods.
- Be suspicious of backtests that are too good: overfitting, survivorship and unrealistic
  execution.

## Exercise

Implement the crossover signal, the position without look-ahead, the returns net of costs, a
summary compared with buy & hold, and the equity curve.

**Further reading:** M. López de Prado, *Advances in Financial Machine Learning*, ch. 11
("The Dangers of Backtesting"); [vectorbt](https://vectorbt.dev/).
