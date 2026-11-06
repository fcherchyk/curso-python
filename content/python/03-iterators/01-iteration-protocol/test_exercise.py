import itertools

import pytest
from exercise import Contador, CuentaRegresiva, primero, totales_y_porcentajes


def test_cuenta_regresiva_se_puede_recorrer_dos_veces():
    c = CuentaRegresiva(3)
    assert list(c) == [3, 2, 1]
    assert list(c) == [3, 2, 1]
    assert list(CuentaRegresiva(0)) == []


def test_cuenta_regresiva_iteradores_independientes():
    c = CuentaRegresiva(2)
    a, b = iter(c), iter(c)
    assert next(a) == 2
    assert next(b) == 2


def test_contador_es_iterador():
    c = Contador(2, 5)
    assert iter(c) is c
    assert next(c) == 2
    assert list(c) == [3, 4]
    assert list(c) == [], "un iterador se consume una sola vez"
    with pytest.raises(StopIteration):
        next(c)


def test_primero():
    assert primero([7, 8]) == 7
    assert primero(x for x in range(10) if x > 3) == 4
    assert primero([], default="nada") == "nada"
    assert primero([]) is None


def test_primero_con_infinito():
    assert primero(itertools.count(100)) == 100


def test_totales_y_porcentajes_con_lista():
    assert totales_y_porcentajes([1, 1, 2]) == [25.0, 25.0, 50.0]


def test_totales_y_porcentajes_con_generador():
    montos = (m for m in [10, 30])
    assert totales_y_porcentajes(montos) == [25.0, 75.0]


def test_totales_y_porcentajes_total_cero():
    assert totales_y_porcentajes([0, 0]) == [0.0, 0.0]
    assert totales_y_porcentajes([]) == []
