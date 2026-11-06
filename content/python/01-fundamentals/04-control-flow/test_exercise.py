import pytest
from exercise import classify_temperature, collatz_steps, fizzbuzz, is_prime


def test_classify_temperature():
    assert classify_temperature(-5) == "cold"
    assert classify_temperature(9.9) == "cold"
    assert classify_temperature(10) == "mild"
    assert classify_temperature(24.9) == "mild"
    assert classify_temperature(25) == "hot"


def test_is_prime():
    assert [x for x in range(30) if is_prime(x)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert not is_prime(-7)
    assert is_prime(7919)
    assert not is_prime(7917)


def test_collatz_steps():
    assert collatz_steps(1) == 0
    assert collatz_steps(6) == 8
    assert collatz_steps(27) == 111


def test_collatz_steps_invalid():
    with pytest.raises(ValueError):
        collatz_steps(0)


def test_fizzbuzz():
    res = fizzbuzz(15)
    assert res[:5] == ["1", "2", "Fizz", "4", "Buzz"]
    assert res[14] == "FizzBuzz"
    assert len(res) == 15
    assert fizzbuzz(0) == []
