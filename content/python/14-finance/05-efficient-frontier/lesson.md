# The efficient frontier with Monte Carlo

The previous chapter computed the risk and return of **one** portfolio. The natural question
is: **what are the best weights?** Harry Markowitz answered it in 1952 (and won the Nobel): there
is no single "best", but an **efficient frontier**, the set of portfolios that give the highest
possible return for each level of risk.

## The idea with Monte Carlo

The rigorous way is an optimization problem (`scipy.optimize.minimize` or `cvxpy`). The intuitive
way, and the one we use here, is to **try lots of random portfolios** and look at the cloud:

```python
rng = np.random.default_rng(42)            # seed: reproducible results
W = rng.random((5000, 4))                  # 5000 portfolios × 4 assets, in [0, 1)
W /= W.sum(axis=1, keepdims=True)          # normalize: each row adds up to 1 (no short selling)
```

`keepdims=True` keeps the sum with shape `(5000, 1)`, so **broadcasting** from module 11 divides
each row by its own sum.

## Return and volatility of 5000 portfolios at once

No `for` loops: NumPy vectorization computes them all together.

```python
mu = r.mean().to_numpy() * 252            # expected annual returns (4,)
cov = r.cov().to_numpy() * 252            # annual covariance (4, 4)

returns = W @ mu                                           # (5000,)
vols = np.sqrt(np.einsum("ij,jk,ik->i", W, cov, W))       # wᵢᵀ Σ wᵢ for each row
sharpes = (returns - 0.04) / vols
```

`einsum` describes the operation with indices: for each portfolio `i`, it sums `W[i,j]·cov[j,k]·W[i,k]`
over `j` and `k`. It's `wᵀΣw` applied row by row. An equivalent alternative is
`((W @ cov) * W).sum(axis=1)`.

## The two notable portfolios

```python
i = sharpes.argmax()      # maximum Sharpe: the best return per unit of risk
j = vols.argmin()         # minimum variance: the least risky
```

| | ACME | BETA | CIRC | DELTA | return | vol | Sharpe |
|---|---|---|---|---|---|---|---|
| maximum Sharpe   | 0.087 | 0.023 | 0.055 | 0.835 | 0.146 | 0.112 | 0.95 |
| minimum variance | 0.053 | 0.252 | 0.006 | 0.689 | 0.104 | 0.107 | 0.59 |

Both load up on DELTA: low volatility, good return and little correlation with the rest.

## The cloud and its edge


When you plot volatility (X) against return (Y), the cloud has an **upper-left edge**: that's
the efficient frontier. Any portfolio below it is **inefficient**, because there's another one
with the same risk and more return. The maximum-Sharpe portfolio is the point on the frontier
where it touches the line coming out of the risk-free rate (the *capital market line*).

## Important caveats

- **The inputs are historical estimates**, and expected returns are extremely noisy. With a
  different period, the "optimal" weights change completely. Markowitz optimization is famous
  for **amplifying estimation errors** ("error maximization").
- That's why, in practice, people use constraints (maximum weights), more robust estimators, or
  approaches that don't depend on expected returns (minimum variance, *risk parity*).
- Monte Carlo is approximate: with many assets, random portfolios almost never reach the edge.
  That's when you need an optimizer.

## Summary

- Generate random weights with `default_rng(seed)` and normalize the rows with `keepdims=True`.
- Returns: `W @ mu`. Variances: `einsum("ij,jk,ik->i", W, cov, W)`.
- Maximum Sharpe with `argmax`, and minimum variance with `argmin` over the volatility.
- The frontier is the upper edge of the risk-return cloud.
- Optimal weights are very sensitive to the estimates: don't trust them blindly.

## Exercise

Generate reproducible random weights, simulate portfolios, find the maximum-Sharpe and
minimum-variance ones, and plot the cloud marking both.

**Further reading:** [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/) (real
optimization); [numpy.einsum](https://numpy.org/doc/stable/reference/generated/numpy.einsum.html).
