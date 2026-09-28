import pytest
from ejercicio import diferencias, emparejar, indices_de, numerar_lineas


def test_indices_de():
    assert indices_de(["a", "b", "a", "c", "a"], "a") == [0, 2, 4]
    assert indices_de(["a"], "z") == []


def test_emparejar():
    assert emparejar(["ana", "beto"], [9.5, 7]) == {"ana": 9.5, "beto": 7}


def test_emparejar_largos_distintos():
    with pytest.raises(ValueError):
        emparejar(["ana"], [1, 2])
    with pytest.raises(ValueError):
        emparejar(["ana", "beto"], [1])


def test_diferencias():
    assert diferencias([18, 21, 19, 25]) == [3, -2, 6]
    assert diferencias([5]) == []
    assert diferencias([]) == []


def test_numerar_lineas():
    assert numerar_lineas(["hola", "chau"]) == ["  1 | hola", "  2 | chau"]


def test_numerar_lineas_con_inicio():
    assert numerar_lineas(["x", "y"], inicio=99) == [" 99 | x", "100 | y"]
