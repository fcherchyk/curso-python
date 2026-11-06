# Aggregations, statistics and reproducible randomness

Analyzing data is, to a large extent, **summarizing** it: means, standard deviations, percentiles,
maximums per group. NumPy performs these reductions along any axis of an array. And to simulate
(Monte Carlo, bootstrap, test data) you need **reproducible** random numbers: the same
seed must always produce the same results.

## Reductions

```python
v = np.array([4, 8, 15, 16, 23, 42])
v.sum(), v.mean(), v.min(), v.max()
v.std()                 # population standard deviation (ddof=0)
v.std(ddof=1)           # sample (divides by n-1): the one pandas and statistics use
np.median(v)
np.percentile(v, [25, 50, 75])     # quartiles
np.cumsum(v)            # cumulative sum: [ 4 12 27 43 66 108]
np.cumprod(1 + rets)    # cumulative product: compound growth
```

> **`ddof`**: by default NumPy uses the **population** standard deviation (`ddof=0`), and pandas
> uses the **sample** one (`ddof=1`). With little data the difference shows. It's a classic source
> of discrepancies between results.

## Reducing along an axis

In a matrix, `axis` says which dimension gets **collapsed**:

```python
# 3 days (rows) x 4 products (columns)
sales = np.array([[5, 2, 0, 7],
                  [3, 8, 1, 2],
                  [6, 1, 4, 9]])

sales.sum(axis=0)       # [14 11  5 18]: total per PRODUCT (collapses the days)
sales.sum(axis=1)       # [14 14 20]: total per DAY (collapses the products)
sales.argmax(axis=0)    # [2 1 2 2]: on which day each product sold the most
sales.max()             # 9: over the whole array
```

Think of it this way: `axis=0` goes **down** (one result per column) and `axis=1` goes **to the
right** (one result per row).

### Missing values: `nan`

```python
v = np.array([1.0, np.nan, 3.0])
v.mean()            # nan  ← a single nan contaminates everything
np.nanmean(v)       # 2.0  ← ignores the nan values
np.isnan(v)         # [False  True False]
```

There are `nan*` versions of almost every reduction (`nansum`, `nanstd`, `nanmax`…). pandas
ignores them by default.

## Random numbers: the modern API

```python
rng = np.random.default_rng(42)        # a seeded generator

rng.random(3)                          # 3 uniform floats in [0, 1)
rng.integers(1, 7, size=10)            # 10 die rolls (7 is excluded)
rng.normal(loc=0, scale=1, size=(2, 3))   # standard normal in a 2x3 matrix
rng.choice(["a", "b", "c"], size=5)    # pick with replacement
rng.choice(v, size=len(v), replace=True)  # resampling (bootstrap)
rng.permutation(v), rng.shuffle(v)
```

- **Use `default_rng`**. The old API (`np.random.seed(...)` + `np.random.rand`) uses a shared
  **global** state: any library that uses it changes your sequence.
- Pass the generator (or the seed) as a **parameter** to your functions. That way tests are
  reproducible and there's no global state.
- The same seed with the same sequence of calls always gives the same result.

```python
def simulate(n: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(size=n)

simulate(3, seed=1) == simulate(3, seed=1)   # all True
```

## Monte Carlo and bootstrap in two lines

```python
# Probability of getting more than 10 when adding two dice
rng = np.random.default_rng(0)
rolls = rng.integers(1, 7, size=(100_000, 2)).sum(axis=1)
(rolls > 10).mean()            # ≈ 0.0833 (3/36)

# Bootstrap: uncertainty of a sample's mean
means = rng.choice(sample, size=(10_000, len(sample))).mean(axis=1)
np.percentile(means, [2.5, 97.5])      # 95% confidence interval
```

Generating **all** the simulations in one matrix and reducing along an axis is much faster than a
loop with one simulation per iteration. It's the same vectorization as before, applied to
statistics. In the finance module we use it for the efficient frontier.

## Summary

- `sum`, `mean`, `std` (`ddof`!), `median`, `percentile`, `cumsum` and `cumprod`.
- `axis=0` gives one result per column and `axis=1` one per row; `argmax(axis=...)` for
  "where".
- `nan` contaminates: use `nanmean` and friends.
- `rng = np.random.default_rng(seed)` and pass it as a parameter; no `np.random.seed`.
- Vectorized Monte Carlo and bootstrap: generate everything in a matrix and reduce.

## Exercise

Summaries along an axis, the best day per product, a dice simulation and a bootstrap, both
reproducible with a seed.

**Further reading:** [Statistics](https://numpy.org/doc/stable/reference/routines.statistics.html),
[Random Generator](https://numpy.org/doc/stable/reference/random/generator.html).
