import itertools

import pytest
from exercise import clamp, deprecated, repeat, retry


def test_repeat():
    counter = itertools.count(1)

    @repeat(3)
    def next_value():
        """Doc."""
        return next(counter)

    assert next_value() == [1, 2, 3]
    assert next_value.__name__ == "next_value"


def test_retry_until_success():
    attempts = []

    @retry(3, exceptions=(ConnectionError,))
    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise ConnectionError
        return "ok"

    assert flaky() == "ok"
    assert len(attempts) == 3


def test_retry_exhausts_and_reraises():
    attempts = []

    @retry(2)
    def always_fails():
        attempts.append(1)
        raise ValueError("nope")

    with pytest.raises(ValueError, match="nope"):
        always_fails()
    assert len(attempts) == 2


def test_retry_does_not_catch_others():
    attempts = []

    @retry(5, exceptions=(ConnectionError,))
    def fails_differently():
        attempts.append(1)
        raise KeyError

    with pytest.raises(KeyError):
        fails_differently()
    assert len(attempts) == 1


def test_clamp():
    @clamp(0, 100)
    def percentage(x):
        return x * 100

    assert percentage(0.5) == 50
    assert percentage(1.5) == 100
    assert percentage(-2) == 0
    assert percentage.__name__ == "percentage"


def test_deprecated_without_parentheses():
    @deprecated
    def old(x):
        return x + 1

    with pytest.warns(DeprecationWarning, match="old is deprecated"):
        assert old(1) == 2
    assert old.__name__ == "old"


def test_deprecated_with_replacement():
    @deprecated(replacement="new")
    def old():
        return "ok"

    with pytest.warns(DeprecationWarning, match="use new"):
        assert old() == "ok"
