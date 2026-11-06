import pytest
from exercise import differences, indices_of, number_lines, pair_up


def test_indices_of():
    assert indices_of(["a", "b", "a", "c", "a"], "a") == [0, 2, 4]
    assert indices_of(["a"], "z") == []


def test_pair_up():
    assert pair_up(["alice", "bob"], [9.5, 7]) == {"alice": 9.5, "bob": 7}


def test_pair_up_different_lengths():
    with pytest.raises(ValueError):
        pair_up(["alice"], [1, 2])
    with pytest.raises(ValueError):
        pair_up(["alice", "bob"], [1])


def test_differences():
    assert differences([18, 21, 19, 25]) == [3, -2, 6]
    assert differences([5]) == []
    assert differences([]) == []


def test_number_lines():
    assert number_lines(["hello", "bye"]) == ["  1 | hello", "  2 | bye"]


def test_number_lines_with_start():
    assert number_lines(["x", "y"], start=99) == [" 99 | x", "100 | y"]
