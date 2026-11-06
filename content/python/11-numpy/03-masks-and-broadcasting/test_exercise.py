import numpy as np
from exercise import (
    center_columns,
    in_range,
    multiplication_table,
    replace_outliers,
    share_above_row_mean,
    top,
)


def test_in_range():
    v = np.array([5, -2, 8, -1, 3, 10])
    np.testing.assert_array_equal(in_range(v, 0, 8), [5, 8, 3])
    assert len(in_range(v, 100, 200)) == 0


def test_replace_outliers_does_not_mutate():
    v = np.array([1.0, -50.0, 3.0, 99.0])
    r = replace_outliers(v, 10)
    np.testing.assert_array_equal(r, [1.0, 0.0, 3.0, 0.0])
    np.testing.assert_array_equal(v, [1.0, -50.0, 3.0, 99.0])


def test_top():
    names = np.array(["alice", "bob", "carol", "dave"])
    scores = np.array([7, 9, 5, 8])
    assert top(names, scores, 2) == ["bob", "dave"]
    assert top(names, scores, 1) == ["bob"]


def test_center_columns():
    m = np.array([[1.0, 10.0], [3.0, 20.0], [5.0, 30.0]])
    r = center_columns(m)
    np.testing.assert_allclose(r, [[-2, -10], [0, 0], [2, 10]])
    np.testing.assert_allclose(r.mean(axis=0), [0, 0])


def test_share_above_row_mean():
    m = np.array([[1, 2, 3, 10], [5, 5, 5, 5]])
    np.testing.assert_allclose(share_above_row_mean(m), [0.25, 0.0])


def test_multiplication_table():
    t = multiplication_table(4)
    assert t.shape == (4, 4)
    assert t[2, 3] == 12
    np.testing.assert_array_equal(t[0], [1, 2, 3, 4])
    np.testing.assert_array_equal(t, t.T)
