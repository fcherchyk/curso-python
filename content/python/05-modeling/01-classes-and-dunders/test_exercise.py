import pytest
from exercise import Carrito, Item, Vector


def test_vector_repr():
    assert repr(Vector(1, 2)) == "Vector(1, 2)"
    assert repr([Vector(0, -1)]) == "[Vector(0, -1)]"


def test_vector_igualdad_y_hash():
    assert Vector(1, 2) == Vector(1, 2)
    assert Vector(1, 2) != Vector(2, 1)
    assert Vector(1, 2) != (1, 2)
    assert len({Vector(1, 2), Vector(1, 2), Vector(3, 4)}) == 2


def test_vector_operadores():
    assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)
    assert Vector(5, 5) - Vector(1, 2) == Vector(4, 3)
    assert Vector(1, 2) * 3 == Vector(3, 6)
    assert 3 * Vector(1, 2) == Vector(3, 6)


def test_vector_tipos_no_soportados():
    with pytest.raises(TypeError):
        Vector(1, 2) + 5
    with pytest.raises(TypeError):
        Vector(1, 2) * "x"


def test_vector_abs_y_bool():
    assert abs(Vector(3, 4)) == 5
    assert bool(Vector(0, 1))
    assert not Vector(0, 0)


def test_carrito():
    c = Carrito().agregar(Item("pan", 1.5, 2)).agregar(Item("leche", 0.99))
    assert c.total == 3.99
    assert len(c) == 3
    assert "pan" in c
    assert "vino" not in c
    assert [i.nombre for i in c] == ["pan", "leche"]
    assert c[1].nombre == "leche"


def test_carrito_vacio_es_falsy():
    assert not Carrito()
    assert Carrito().total == 0


def test_carritos_no_comparten_items():
    a, b = Carrito(), Carrito()
    a.agregar(Item("x", 1))
    assert len(b) == 0
