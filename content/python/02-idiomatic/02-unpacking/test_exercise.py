import pytest
from exercise import extremos, fusionar_config, primero_y_resto, sumar_puntos


def test_primero_y_resto():
    assert primero_y_resto([1, 2, 3]) == (1, [2, 3])
    assert primero_y_resto([7]) == (7, [])


def test_primero_y_resto_vacio():
    with pytest.raises(ValueError):
        primero_y_resto([])


def test_extremos():
    assert extremos([4, 8, 15, 16]) == (4, 16)
    assert extremos([9]) == (9, 9)


def test_extremos_vacio():
    with pytest.raises(ValueError):
        extremos([])


def test_sumar_puntos():
    assert sumar_puntos([(1, 2), (3, 4), (0, -1)]) == (4, 5)
    assert sumar_puntos([]) == (0, 0)


def test_fusionar_config():
    base = {"debug": False, "port": 80}
    extra = {"port": 8080}
    res = fusionar_config(base, extra, {"debug": True, "host": "x"})
    assert res == {"debug": True, "port": 8080, "host": "x"}
    assert base == {"debug": False, "port": 80}, "no hay que mutar base"
    assert extra == {"port": 8080}, "no hay que mutar los overrides"


def test_fusionar_config_sin_overrides_devuelve_copia():
    base = {"a": 1}
    res = fusionar_config(base)
    assert res == base
    assert res is not base
