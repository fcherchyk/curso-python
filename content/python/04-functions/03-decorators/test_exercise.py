import pytest
from exercise import HANDLERS, count_calls, dispatch, handler, memoize


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
    assert slow.__name__ == "slow"


def test_memoize_fibonacci_fast():
    @memoize
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(80) == 23416728348467685


def test_handler_registers_without_wrapping():
    def on_start(x):
        return x * 2

    decorated = handler(on_start)
    assert decorated is on_start
    assert HANDLERS["on_start"] is on_start


def test_dispatch():
    @handler
    def add(a, b):
        return a + b

    assert dispatch("add", 2, 3) == 5


def test_dispatch_missing():
    with pytest.raises(KeyError):
        dispatch("does_not_exist")
