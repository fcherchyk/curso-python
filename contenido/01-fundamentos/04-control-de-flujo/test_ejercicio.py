import pytest
from ejercicio import clasificar_temperatura, es_primo, fizzbuzz, pasos_collatz


def test_clasificar_temperatura():
    assert clasificar_temperatura(-5) == "frío"
    assert clasificar_temperatura(9.9) == "frío"
    assert clasificar_temperatura(10) == "templado"
    assert clasificar_temperatura(24.9) == "templado"
    assert clasificar_temperatura(25) == "calor"


def test_es_primo():
    assert [x for x in range(30) if es_primo(x)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert not es_primo(-7)
    assert es_primo(7919)
    assert not es_primo(7917)


def test_pasos_collatz():
    assert pasos_collatz(1) == 0
    assert pasos_collatz(6) == 8
    assert pasos_collatz(27) == 111


def test_pasos_collatz_invalido():
    with pytest.raises(ValueError):
        pasos_collatz(0)


def test_fizzbuzz():
    res = fizzbuzz(15)
    assert res[:5] == ["1", "2", "Fizz", "4", "Buzz"]
    assert res[14] == "FizzBuzz"
    assert len(res) == 15
    assert fizzbuzz(0) == []
