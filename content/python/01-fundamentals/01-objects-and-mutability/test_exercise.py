from decimal import Decimal

from exercise import append_without_mutating, copy_matrix, split_evenly, sum_prices


def test_append_without_mutating():
    xs = [1, 2]
    res = append_without_mutating(xs, 3)
    assert res == [1, 2, 3]
    assert xs == [1, 2], "the original list must not be mutated"
    assert res is not xs


def test_copy_matrix_is_independent():
    m = [[1, 2], [3, 4]]
    c = copy_matrix(m)
    assert c == m
    c[0].append(99)
    c.append([5])
    assert m == [[1, 2], [3, 4]], "modifying the copy changed the original"


def test_sum_prices_exact():
    assert sum_prices(["0.10", "0.20"]) == Decimal("0.30")
    assert sum_prices(["19.99"] * 3) == Decimal("59.97")
    assert isinstance(sum_prices(["1"]), Decimal)


def test_sum_prices_empty():
    assert sum_prices([]) == 0


def test_split_evenly():
    assert split_evenly(17, 5) == (3, 2)
    assert split_evenly(10, 5) == (2, 0)


def test_split_evenly_negative_satisfies_identity():
    each, leftover = split_evenly(-7, 2)
    assert each * 2 + leftover == -7
    assert (each, leftover) == (-4, 1)
