"""Aggregations, statistics and reproducible randomness. No Python loops."""

import numpy as np


def column_summary(m: np.ndarray) -> dict[str, np.ndarray]:
    """{"mean", "std", "min", "max"} of each column.
    The standard deviation is the SAMPLE one (ddof=1). Ignore nan values (nan* functions).
    """
    raise NotImplementedError("TODO")


def best_day_per_product(sales: np.ndarray, days: np.ndarray) -> list[str]:
    """sales: rows = days, columns = products. For each product, the name of the day
    it sold the most (argmax along an axis + fancy indexing).
    """
    raise NotImplementedError("TODO")


def dice_sum_prob(target: int, n: int, seed: int) -> float:
    """Monte Carlo estimate of the probability that the sum of TWO dice is `target`.
    Simulate n rolls all at once with np.random.default_rng(seed).
    """
    raise NotImplementedError("TODO")


def bootstrap_interval(sample: np.ndarray, n: int, seed: int) -> tuple[float, float]:
    """95% interval for the MEAN via bootstrap: n resamples with replacement of the same
    size as the sample (an n x len(sample) matrix), mean per row, and percentiles 2.5 and 97.5.
    """
    raise NotImplementedError("TODO")
