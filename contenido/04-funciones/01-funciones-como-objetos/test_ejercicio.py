import pytest
from ejercicio import aplicar_n_veces, calcular, componer, parseador_de_base


def test_componer():
    def doble(x):
        return x * 2

    def mas_uno(x):
        return x + 1

    assert componer(doble, mas_uno)(3) == 8  # doble(mas_uno(3))
    assert componer(mas_uno, doble)(3) == 7
    assert componer()(42) == 42


def test_aplicar_n_veces():
    assert aplicar_n_veces(lambda v: v * 2, 3, 1) == 8
    assert aplicar_n_veces(str.upper, 0, "x") == "x"


def test_calcular():
    assert calcular("+", 2, 3) == 5
    assert calcular("-", 2, 3) == -1
    assert calcular("*", 2, 3) == 6
    assert calcular("/", 3, 2) == 1.5
    assert calcular("**", 2, 10) == 1024


def test_calcular_operacion_desconocida():
    with pytest.raises(ValueError):
        calcular("%", 1, 2)


def test_parseador_de_base():
    assert parseador_de_base(2)("1010") == 10
    assert parseador_de_base(16)("ff") == 255
    with pytest.raises(ValueError):
        parseador_de_base(2)("12")
