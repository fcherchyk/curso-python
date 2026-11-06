import pytest
from exercise import apply_n_times, base_parser, calculate, compose


def test_compose():
    def double(x):
        return x * 2

    def plus_one(x):
        return x + 1

    assert compose(double, plus_one)(3) == 8  # double(plus_one(3))
    assert compose(plus_one, double)(3) == 7
    assert compose()(42) == 42


def test_apply_n_times():
    assert apply_n_times(lambda v: v * 2, 3, 1) == 8
    assert apply_n_times(str.upper, 0, "x") == "x"


def test_calculate():
    assert calculate("+", 2, 3) == 5
    assert calculate("-", 2, 3) == -1
    assert calculate("*", 2, 3) == 6
    assert calculate("/", 3, 2) == 1.5
    assert calculate("**", 2, 10) == 1024


def test_calculate_unknown_operation():
    with pytest.raises(ValueError):
        calculate("%", 1, 2)


def test_base_parser():
    assert base_parser(2)("1010") == 10
    assert base_parser(16)("ff") == 255
    with pytest.raises(ValueError):
        base_parser(2)("12")
