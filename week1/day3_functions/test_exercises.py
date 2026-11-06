import time
from pathlib import Path

import pytest

from week1.day3_functions.exercises import (
    Timer,
    capture_errors,
    compose,
    count_calls,
    in_directory,
    make_counter,
    memoize,
    retry,
)


def test_make_counter_independent():
    a, b = make_counter(), make_counter(10)
    assert [a(), a(), a()] == [0, 1, 2]
    assert [b(), b()] == [10, 11]
    assert a() == 3


def test_compose():
    def double(x):
        return x * 2

    def plus_one(x):
        return x + 1

    assert compose(double, plus_one)(3) == 8  # double(plus_one(3))
    assert compose(plus_one, double)(3) == 7
    assert compose()(42) == 42


def test_count_calls():
    @count_calls
    def greet(name):
        """Greets."""
        return f"hello {name}"

    assert greet.calls == 0
    assert greet("alice") == "hello alice"
    greet(name="bob")
    assert greet.calls == 2
    assert greet.__name__ == "greet"
    assert greet.__doc__ == "Greets."


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


def test_retry_runs_out_and_reraises():
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


def test_memoize():
    calls = []

    @memoize
    def slow(a, b):
        calls.append((a, b))
        return a + b

    assert slow(1, 2) == 3
    assert slow(1, 2) == 3
    assert slow(2, 1) == 3
    assert calls == [(1, 2), (2, 1)]
    assert len(slow.cache) == 2


def test_memoize_fast_fibonacci():
    @memoize
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(80) == 23416728348467685


def test_timer():
    t = Timer()
    assert t.duration is None
    with t as same:
        assert same is t
        time.sleep(0.01)
    assert 0.005 < t.duration < 1


def test_timer_does_not_suppress():
    t = Timer()
    with pytest.raises(RuntimeError), t:
        raise RuntimeError
    assert t.duration is not None


def test_in_directory(tmp_path):
    original = Path.cwd()
    with in_directory(tmp_path) as p:
        assert Path.cwd() == tmp_path.resolve()
        assert p == tmp_path
    assert Path.cwd() == original


def test_in_directory_restores_on_exception(tmp_path):
    original = Path.cwd()
    with pytest.raises(ZeroDivisionError), in_directory(tmp_path):
        1 / 0
    assert Path.cwd() == original


def test_capture_errors():
    with capture_errors(ValueError, KeyError) as errors:
        int("not a number")
    assert len(errors) == 1
    assert isinstance(errors[0], ValueError)

    with capture_errors(ValueError) as errors:
        pass
    assert errors == []

    with pytest.raises(TypeError), capture_errors(ValueError):
        raise TypeError
