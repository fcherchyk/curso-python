import pytest
from exercise import Temperatura, Usuario


def test_temperatura_celsius_y_fahrenheit():
    t = Temperatura(100)
    assert t.celsius == 100
    assert t.fahrenheit == 212


def test_temperatura_setter_fahrenheit_actualiza_celsius():
    t = Temperatura(0)
    t.fahrenheit = 50
    assert t.celsius == pytest.approx(10)


def test_temperatura_valida_al_construir_y_asignar():
    with pytest.raises(ValueError):
        Temperatura(-300)
    t = Temperatura(20)
    with pytest.raises(ValueError):
        t.celsius = -274


def test_temperatura_desde_fahrenheit():
    t = Temperatura.desde_fahrenheit(32)
    assert isinstance(t, Temperatura)
    assert t.celsius == pytest.approx(0)


def test_desde_fahrenheit_respeta_subclases():
    class TemperaturaAmbiente(Temperatura):
        pass

    assert type(TemperaturaAmbiente.desde_fahrenheit(68)) is TemperaturaAmbiente


def test_usuario_email_normalizado():
    u = Usuario(1, "  Ana@Mail.COM ")
    assert u.email == "ana@mail.com"
    u.email = "BETO@x.org"
    assert u.email == "beto@x.org"


def test_usuario_email_invalido():
    with pytest.raises(ValueError):
        Usuario(1, "sin-arroba")
    u = Usuario(1, "a@b.c")
    with pytest.raises(ValueError):
        u.email = "nop"


def test_usuario_id_solo_lectura():
    u = Usuario(7, "a@b.c")
    assert u.id == 7
    with pytest.raises(AttributeError):
        u.id = 8


def test_usuario_normalizar_email_es_estatico():
    assert Usuario.normalizar_email(" X@Y.Z ") == "x@y.z"


def test_usuario_desde_dict():
    u = Usuario.desde_dict({"id": 3, "email": "C@D.E"})
    assert (u.id, u.email) == (3, "c@d.e")
