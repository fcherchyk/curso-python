"""Tests de referencia para calendario.py."""

import pytest
from calendario import dias_del_mes, es_bisiesto


@pytest.mark.parametrize(
    ("anio", "esperado"),
    [
        pytest.param(2024, True, id="divisible-por-4"),
        pytest.param(2023, False, id="comun"),
        pytest.param(1900, False, id="siglo-no-bisiesto"),
        pytest.param(2000, True, id="divisible-por-400"),
    ],
)
def test_es_bisiesto(anio, esperado):
    assert es_bisiesto(anio) is esperado


@pytest.mark.parametrize(
    ("mes", "dias"),
    [(1, 31), (4, 30), (6, 30), (9, 30), (11, 30), (12, 31)],
)
def test_dias_de_meses_no_febrero(mes, dias):
    assert dias_del_mes(2023, mes) == dias


def test_febrero():
    assert dias_del_mes(2024, 2) == 29
    assert dias_del_mes(2023, 2) == 28
    assert dias_del_mes(1900, 2) == 28


@pytest.mark.parametrize("mes", [0, 13, -1])
def test_mes_invalido(mes):
    with pytest.raises(ValueError, match="mes inválido"):
        dias_del_mes(2024, mes)
