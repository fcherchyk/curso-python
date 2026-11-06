import itertools
import types

import pytest

from week1.day2_iterators.exercises import (
    Countdown,
    ManualCounter,
    combinations_summing_to,
    deep_flatten,
    fibonacci,
    first_even_squares,
    in_batches,
    run_length_encode,
    sliding_windows,
    useful_lines,
)


def test_countdown_can_be_iterated_twice():
    c = Countdown(3)
    assert list(c) == [3, 2, 1]
    assert list(c) == [3, 2, 1]
    assert list(Countdown(0)) == []


def test_manual_counter_is_an_iterator():
    c = ManualCounter(2, 5)
    assert iter(c) is c
    assert next(c) == 2
    assert list(c) == [3, 4]
    assert list(c) == [], "an iterator can be consumed only once"
    with pytest.raises(StopIteration):
        next(c)


def test_fibonacci():
    assert list(itertools.islice(fibonacci(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert isinstance(fibonacci(), types.GeneratorType)


def test_useful_lines():
    lines_in = ["  a  ", "", "# comment", "   ", "  # another", "b\n"]
    result = useful_lines(lines_in)
    assert isinstance(result, types.GeneratorType), "it must be a generator"
    assert list(result) == ["a", "b"]


def test_deep_flatten():
    assert list(deep_flatten([1, [2, (3, [4, [5]])], "ab", []])) == [1, 2, 3, 4, 5, "ab"]


def test_in_batches_with_iterator():
    assert list(in_batches(iter(range(7)), 3)) == [(0, 1, 2), (3, 4, 5), (6,)]
    assert list(in_batches([], 3)) == []


def test_in_batches_is_lazy():
    batches = in_batches(itertools.count(), 2)
    assert next(batches) == (0, 1)
    assert next(batches) == (2, 3)


def test_sliding_windows():
    assert list(sliding_windows([1, 2, 3, 4, 5], 3)) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    assert list(sliding_windows([1, 2], 3)) == []


def test_run_length_encode():
    assert run_length_encode("aaabccaa") == [("a", 3), ("b", 1), ("c", 2), ("a", 2)]
    assert run_length_encode("") == []


def test_combinations_summing_to():
    assert combinations_summing_to([1, 2, 3, 4, 5], 2, 6) == [(1, 5), (2, 4)]
    assert combinations_summing_to([1, 2, 3, 4, 5], 3, 9) == [(1, 3, 5), (2, 3, 4)]


def test_first_even_squares_with_infinite_input():
    assert first_even_squares(itertools.count(1), 4) == [4, 16, 36, 64]
