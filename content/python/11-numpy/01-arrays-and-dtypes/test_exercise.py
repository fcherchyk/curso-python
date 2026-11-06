import numpy as np
from exercise import edges, grid, normalized_copy, points, zero_the_middle


def test_grid():
    t = grid(2, 3)
    assert t.shape == (2, 3)
    assert t.dtype == np.int64
    np.testing.assert_array_equal(t, [[1, 2, 3], [4, 5, 6]])
    assert grid(3, 1).tolist() == [[1], [2], [3]]


def test_points():
    p = points(0, 1, 5)
    assert p.dtype == np.float64
    np.testing.assert_allclose(p, [0, 0.25, 0.5, 0.75, 1])
    assert len(points(-1, 1, 11)) == 11


def test_edges():
    m = np.arange(1, 10).reshape(3, 3)
    col, row, diag = edges(m)
    np.testing.assert_array_equal(col, [1, 4, 7])
    np.testing.assert_array_equal(row, [7, 8, 9])
    np.testing.assert_array_equal(diag, [1, 5, 9])


def test_normalized_copy_does_not_modify():
    base = np.array([1, 2, 4, 8])
    view = base[1:]
    r = normalized_copy(view)
    np.testing.assert_allclose(r, [0.25, 0.5, 1.0])
    assert r.dtype == np.float64
    np.testing.assert_array_equal(base, [1, 2, 4, 8])


def test_zero_the_middle_in_place():
    base = np.arange(10)
    view = base[2:8]  # [2 3 4 5 6 7]
    assert zero_the_middle(view) is None
    np.testing.assert_array_equal(view, [2, 0, 0, 0, 0, 7])
    np.testing.assert_array_equal(base, [0, 1, 2, 0, 0, 0, 0, 7, 8, 9])  # the view shares data
