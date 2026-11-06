import numpy as np
import pytest
from exercise import (
    best_day_per_product,
    bootstrap_interval,
    column_summary,
    dice_sum_prob,
)


def test_column_summary():
    m = np.array([[1.0, 10.0], [3.0, np.nan], [5.0, 30.0]])
    r = column_summary(m)
    np.testing.assert_allclose(r["mean"], [3.0, 20.0])
    np.testing.assert_allclose(r["std"], [2.0, np.std([10, 30], ddof=1)])
    np.testing.assert_allclose(r["min"], [1.0, 10.0])
    np.testing.assert_allclose(r["max"], [5.0, 30.0])


def test_best_day_per_product():
    sales = np.array([[5, 2, 0, 7], [3, 8, 1, 2], [6, 1, 4, 9]])
    days = np.array(["mon", "tue", "wed"])
    assert best_day_per_product(sales, days) == ["wed", "tue", "wed", "wed"]


def test_dice_sum_prob():
    p = dice_sum_prob(7, 200_000, seed=1)
    assert p == pytest.approx(1 / 6, abs=0.01)
    assert dice_sum_prob(12, 200_000, seed=1) == pytest.approx(1 / 36, abs=0.005)
    assert dice_sum_prob(13, 1000, seed=1) == 0.0


def test_dice_sum_prob_is_reproducible():
    assert dice_sum_prob(7, 1000, seed=5) == dice_sum_prob(7, 1000, seed=5)


def test_bootstrap_interval():
    sample = np.random.default_rng(0).normal(loc=50, scale=10, size=200)
    low, high = bootstrap_interval(sample, 5000, seed=3)
    assert low < sample.mean() < high
    assert 2 < high - low < 4  # ≈ 2 * 1.96 * 10 / sqrt(200) ≈ 2.8
    assert bootstrap_interval(sample, 500, seed=9) == bootstrap_interval(sample, 500, seed=9)
