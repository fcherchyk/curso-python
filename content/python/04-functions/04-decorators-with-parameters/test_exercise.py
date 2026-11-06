import itertools

import pytest
from exercise import acotar, deprecado, reintentar, repetir


def test_repetir():
    contador = itertools.count(1)

    @repetir(3)
    def siguiente():
        """Doc."""
        return next(contador)

    assert siguiente() == [1, 2, 3]
    assert siguiente.__name__ == "siguiente"


def test_reintentar_hasta_exito():
    intentos = []

    @reintentar(3, excepciones=(ConnectionError,))
    def inestable():
        intentos.append(1)
        if len(intentos) < 3:
            raise ConnectionError
        return "ok"

    assert inestable() == "ok"
    assert len(intentos) == 3


def test_reintentar_agota_y_relevanta():
    intentos = []

    @reintentar(2)
    def siempre_falla():
        intentos.append(1)
        raise ValueError("nop")

    with pytest.raises(ValueError, match="nop"):
        siempre_falla()
    assert len(intentos) == 2


def test_reintentar_no_captura_otras():
    intentos = []

    @reintentar(5, excepciones=(ConnectionError,))
    def falla_distinto():
        intentos.append(1)
        raise KeyError

    with pytest.raises(KeyError):
        falla_distinto()
    assert len(intentos) == 1


def test_acotar():
    @acotar(0, 100)
    def porcentaje(x):
        return x * 100

    assert porcentaje(0.5) == 50
    assert porcentaje(1.5) == 100
    assert porcentaje(-2) == 0
    assert porcentaje.__name__ == "porcentaje"


def test_deprecado_sin_parentesis():
    @deprecado
    def vieja(x):
        return x + 1

    with pytest.warns(DeprecationWarning, match="vieja está deprecada"):
        assert vieja(1) == 2
    assert vieja.__name__ == "vieja"


def test_deprecado_con_reemplazo():
    @deprecado(reemplazo="nueva")
    def vieja():
        return "ok"

    with pytest.warns(DeprecationWarning, match="usá nueva"):
        assert vieja() == "ok"
