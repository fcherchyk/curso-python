import time

import numpy as np
import pytest
from exercise import changes, final_prices, invoice_total, normalize, sum_of_squares


def test_invoice_total():
    prices = np.array([100.0, 250.0, 80.0])
    quantities = np.array([2, 1, 5])
    assert invoice_total(prices, quantities) == pytest.approx(1028.5)
    assert invoice_total(prices, quantities, tax=0) == pytest.approx(850.0)


def test_normalize():
    np.testing.assert_allclose(normalize(np.array([10, 20, 30])), [0, 0.5, 1])
    r = normalize(np.array([5, 5, 5]))
    np.testing.assert_array_equal(r, [0.0, 0.0, 0.0])
    assert r.dtype == np.float64


def test_final_prices():
    r = final_prices(np.array([100.0, 300.0, 2000.0, -5.0]), threshold=200)
    np.testing.assert_allclose(r, [100.0, 270.0, 1000.0, 0.0])


def test_changes():
    np.testing.assert_allclose(changes(np.array([100, 110, 99])), [0.1, -0.1])
    assert len(changes(np.arange(1, 11))) == 9


def test_sum_of_squares_is_correct():
    assert sum_of_squares(np.array([1.0, 2.0, 3.0])) == pytest.approx(14.0)


def test_sum_of_squares_is_vectorized():
    v = np.random.default_rng(0).random(500_000)
    start = time.perf_counter()
    slow = sum(x * x for x in v)
    t_loop = time.perf_counter() - start

    start = time.perf_counter()
    fast = sum_of_squares(v)
    t_numpy = time.perf_counter() - start

    assert fast == pytest.approx(slow)
    assert t_numpy < t_loop / 5, f"numpy {t_numpy:.4f}s vs loop {t_loop:.4f}s: did you use a for loop?"
