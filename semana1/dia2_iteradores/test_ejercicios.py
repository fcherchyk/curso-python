import itertools
import types

import pytest

from semana1.dia2_iteradores.ejercicios import (
    Contador,
    CuentaRegresiva,
    aplanar_profundo,
    combinaciones_que_suman,
    comprimir_repetidos,
    en_lotes,
    fibonacci,
    lineas_utiles,
    primeros_cuadrados_pares,
    ventanas,
)


def test_cuenta_regresiva_se_puede_recorrer_dos_veces():
    c = CuentaRegresiva(3)
    assert list(c) == [3, 2, 1]
    assert list(c) == [3, 2, 1]
    assert list(CuentaRegresiva(0)) == []


def test_contador_es_iterador():
    c = Contador(2, 5)
    assert iter(c) is c
    assert next(c) == 2
    assert list(c) == [3, 4]
    assert list(c) == [], "un iterador se consume una sola vez"
    with pytest.raises(StopIteration):
        next(c)


def test_fibonacci():
    assert list(itertools.islice(fibonacci(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert isinstance(fibonacci(), types.GeneratorType)


def test_lineas_utiles():
    entrada = ["  a  ", "", "# comentario", "   ", "  # otro", "b\n"]
    resultado = lineas_utiles(entrada)
    assert isinstance(resultado, types.GeneratorType), "tiene que ser un generador"
    assert list(resultado) == ["a", "b"]


def test_aplanar_profundo():
    assert list(aplanar_profundo([1, [2, (3, [4, [5]])], "ab", []])) == [1, 2, 3, 4, 5, "ab"]


def test_en_lotes_con_iterador():
    assert list(en_lotes(iter(range(7)), 3)) == [(0, 1, 2), (3, 4, 5), (6,)]
    assert list(en_lotes([], 3)) == []


def test_en_lotes_es_perezoso():
    lotes = en_lotes(itertools.count(), 2)
    assert next(lotes) == (0, 1)
    assert next(lotes) == (2, 3)


def test_ventanas():
    assert list(ventanas([1, 2, 3, 4, 5], 3)) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    assert list(ventanas([1, 2], 3)) == []


def test_comprimir_repetidos():
    assert comprimir_repetidos("aaabccaa") == [("a", 3), ("b", 1), ("c", 2), ("a", 2)]
    assert comprimir_repetidos("") == []


def test_combinaciones_que_suman():
    assert combinaciones_que_suman([1, 2, 3, 4, 5], 2, 6) == [(1, 5), (2, 4)]
    assert combinaciones_que_suman([1, 2, 3, 4, 5], 3, 9) == [(1, 3, 5), (2, 3, 4)]


def test_primeros_cuadrados_pares_con_infinito():
    assert primeros_cuadrados_pares(itertools.count(1), 4) == [4, 16, 36, 64]
