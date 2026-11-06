import itertools
import types

import pytest
from exercise import decimal_range, deep_flatten, fibonacci, useful_lines


def test_fibonacci():
    assert list(itertools.islice(fibonacci(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert isinstance(fibonacci(), types.GeneratorType)


def test_useful_lines():
    lines = ["  a  ", "", "# comment", "   ", "  # another", "b\n"]
    result = useful_lines(lines)
    assert isinstance(result, types.GeneratorType), "it must be a generator"
    assert list(result) == ["a", "b"]


def test_useful_lines_is_lazy():
    def source():
        yield "one"
        raise AssertionError("read too far")

    assert next(useful_lines(source())) == "one"


def test_deep_flatten():
    data = [1, [2, (3, [4, [5]])], "ab", []]
    assert list(deep_flatten(data)) == [1, 2, 3, 4, 5, "ab"]
    assert isinstance(deep_flatten([]), types.GeneratorType)


def test_decimal_range():
    assert list(decimal_range(0, 0.5, 0.1)) == [0.0, 0.1, 0.2, 0.3, 0.4]
    assert list(decimal_range(1, 1, 0.5)) == []
    assert len(list(decimal_range(0, 1, 0.01))) == 100


def test_decimal_range_invalid_step():
    gen = decimal_range(0, 1, 0)
    assert isinstance(gen, types.GeneratorType)
    with pytest.raises(ValueError):
        next(gen)
