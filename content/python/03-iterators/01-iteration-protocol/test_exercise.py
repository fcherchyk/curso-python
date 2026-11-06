import itertools

import pytest
from exercise import Countdown, Counter, first, totals_and_percentages


def test_countdown_can_be_iterated_twice():
    c = Countdown(3)
    assert list(c) == [3, 2, 1]
    assert list(c) == [3, 2, 1]
    assert list(Countdown(0)) == []


def test_countdown_independent_iterators():
    c = Countdown(2)
    a, b = iter(c), iter(c)
    assert next(a) == 2
    assert next(b) == 2


def test_counter_is_iterator():
    c = Counter(2, 5)
    assert iter(c) is c
    assert next(c) == 2
    assert list(c) == [3, 4]
    assert list(c) == [], "an iterator is consumed only once"
    with pytest.raises(StopIteration):
        next(c)


def test_first():
    assert first([7, 8]) == 7
    assert first(x for x in range(10) if x > 3) == 4
    assert first([], default="nothing") == "nothing"
    assert first([]) is None


def test_first_with_infinite():
    assert first(itertools.count(100)) == 100


def test_totals_and_percentages_with_list():
    assert totals_and_percentages([1, 1, 2]) == [25.0, 25.0, 50.0]


def test_totals_and_percentages_with_generator():
    amounts = (a for a in [10, 30])
    assert totals_and_percentages(amounts) == [25.0, 75.0]


def test_totals_and_percentages_zero_total():
    assert totals_and_percentages([0, 0]) == [0.0, 0.0]
    assert totals_and_percentages([]) == []
