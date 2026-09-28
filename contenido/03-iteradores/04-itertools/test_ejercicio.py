import itertools

from ejercicio import combinaciones_que_suman, comprimir_repetidos, saldos, ventanas


def test_ventanas():
    assert list(ventanas([1, 2, 3, 4, 5], 3)) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    assert list(ventanas([1, 2], 3)) == []


def test_ventanas_perezoso_con_infinito():
    v = ventanas(itertools.count(), 2)
    assert next(v) == (0, 1)
    assert next(v) == (1, 2)


def test_comprimir_repetidos():
    assert comprimir_repetidos("aaabccaa") == [("a", 3), ("b", 1), ("c", 2), ("a", 2)]
    assert comprimir_repetidos("") == []


def test_combinaciones_que_suman():
    assert combinaciones_que_suman([1, 2, 3, 4, 5], 2, 6) == [(1, 5), (2, 4)]
    assert combinaciones_que_suman([1, 2, 3, 4, 5], 3, 9) == [(1, 3, 5), (2, 3, 4)]
    assert combinaciones_que_suman([1, 2], 3, 3) == []


def test_saldos():
    assert saldos(1000, [100, -30, 50]) == [1000, 1100, 1070, 1120]
    assert saldos(5, []) == [5]
