import itertools

from exercise import balances, combinations_that_sum, compress_runs, windows


def test_windows():
    assert list(windows([1, 2, 3, 4, 5], 3)) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    assert list(windows([1, 2], 3)) == []


def test_windows_lazy_with_infinite():
    w = windows(itertools.count(), 2)
    assert next(w) == (0, 1)
    assert next(w) == (1, 2)


def test_compress_runs():
    assert compress_runs("aaabccaa") == [("a", 3), ("b", 1), ("c", 2), ("a", 2)]
    assert compress_runs("") == []


def test_combinations_that_sum():
    assert combinations_that_sum([1, 2, 3, 4, 5], 2, 6) == [(1, 5), (2, 4)]
    assert combinations_that_sum([1, 2, 3, 4, 5], 3, 9) == [(1, 3, 5), (2, 3, 4)]
    assert combinations_that_sum([1, 2], 3, 3) == []


def test_balances():
    assert balances(1000, [100, -30, 50]) == [1000, 1100, 1070, 1120]
    assert balances(5, []) == [5]
