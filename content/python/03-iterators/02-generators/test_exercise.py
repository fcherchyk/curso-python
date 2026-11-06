import itertools
import types

import pytest
from exercise import aplanar_profundo, fibonacci, lineas_utiles, rango_decimal


def test_fibonacci():
    assert list(itertools.islice(fibonacci(), 10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert isinstance(fibonacci(), types.GeneratorType)


def test_lineas_utiles():
    entrada = ["  a  ", "", "# comentario", "   ", "  # otro", "b\n"]
    resultado = lineas_utiles(entrada)
    assert isinstance(resultado, types.GeneratorType), "tiene que ser un generador"
    assert list(resultado) == ["a", "b"]


def test_lineas_utiles_es_perezoso():
    def fuente():
        yield "uno"
        raise AssertionError("se leyó de más")

    assert next(lineas_utiles(fuente())) == "uno"


def test_aplanar_profundo():
    datos = [1, [2, (3, [4, [5]])], "ab", []]
    assert list(aplanar_profundo(datos)) == [1, 2, 3, 4, 5, "ab"]
    assert isinstance(aplanar_profundo([]), types.GeneratorType)


def test_rango_decimal():
    assert list(rango_decimal(0, 0.5, 0.1)) == [0.0, 0.1, 0.2, 0.3, 0.4]
    assert list(rango_decimal(1, 1, 0.5)) == []
    assert len(list(rango_decimal(0, 1, 0.01))) == 100


def test_rango_decimal_paso_invalido():
    gen = rango_decimal(0, 1, 0)
    assert isinstance(gen, types.GeneratorType)
    with pytest.raises(ValueError):
        next(gen)
