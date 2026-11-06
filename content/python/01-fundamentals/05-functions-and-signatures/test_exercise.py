import pytest
from exercise import agregar_item, crear_usuario, formatear_atributos, promedio


def test_agregar_item_sin_default_compartido():
    assert agregar_item("a") == ["a"]
    assert agregar_item("b") == ["b"]


def test_agregar_item_con_lista():
    xs = ["x"]
    assert agregar_item("y", xs) == ["x", "y"]
    assert xs == ["x", "y"]


def test_promedio():
    assert promedio(1, 2, 3, 4) == 2.5
    assert promedio(7) == 7
    assert promedio(*[2, 4]) == 3


def test_promedio_sin_numeros():
    with pytest.raises(ValueError):
        promedio()


def test_crear_usuario():
    assert crear_usuario("ana", admin=True, email="a@b.c") == {
        "nombre": "ana",
        "admin": True,
        "email": "a@b.c",
    }
    assert crear_usuario("beto") == {"nombre": "beto", "admin": False}


def test_crear_usuario_nombre_solo_posicional():
    with pytest.raises(TypeError):
        crear_usuario(nombre="ana")


def test_crear_usuario_admin_solo_keyword():
    with pytest.raises(TypeError):
        crear_usuario("ana", True)


def test_formatear_atributos():
    assert (
        formatear_atributos(id="x", disabled=True, hidden=False, title="Hola")
        == 'id="x" disabled title="Hola"'
    )
    assert formatear_atributos() == ""
    assert formatear_atributos(n=0, v=None) == 'n="0"'
