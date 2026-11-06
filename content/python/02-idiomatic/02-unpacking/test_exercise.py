import pytest
from exercise import ends, first_and_rest, merge_config, sum_points


def test_first_and_rest():
    assert first_and_rest([1, 2, 3]) == (1, [2, 3])
    assert first_and_rest([7]) == (7, [])


def test_first_and_rest_empty():
    with pytest.raises(ValueError):
        first_and_rest([])


def test_ends():
    assert ends([4, 8, 15, 16]) == (4, 16)
    assert ends([9]) == (9, 9)


def test_ends_empty():
    with pytest.raises(ValueError):
        ends([])


def test_sum_points():
    assert sum_points([(1, 2), (3, 4), (0, -1)]) == (4, 5)
    assert sum_points([]) == (0, 0)


def test_merge_config():
    base = {"debug": False, "port": 80}
    extra = {"port": 8080}
    res = merge_config(base, extra, {"debug": True, "host": "x"})
    assert res == {"debug": True, "port": 8080, "host": "x"}
    assert base == {"debug": False, "port": 80}, "base must not be mutated"
    assert extra == {"port": 8080}, "the overrides must not be mutated"


def test_merge_config_without_overrides_returns_copy():
    base = {"a": 1}
    res = merge_config(base)
    assert res == base
    assert res is not base
