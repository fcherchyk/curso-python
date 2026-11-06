import pytest
from exercise import Cart, Item, Vector


def test_vector_repr():
    assert repr(Vector(1, 2)) == "Vector(1, 2)"
    assert repr([Vector(0, -1)]) == "[Vector(0, -1)]"


def test_vector_equality_and_hash():
    assert Vector(1, 2) == Vector(1, 2)
    assert Vector(1, 2) != Vector(2, 1)
    assert Vector(1, 2) != (1, 2)
    assert len({Vector(1, 2), Vector(1, 2), Vector(3, 4)}) == 2


def test_vector_operators():
    assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)
    assert Vector(5, 5) - Vector(1, 2) == Vector(4, 3)
    assert Vector(1, 2) * 3 == Vector(3, 6)
    assert 3 * Vector(1, 2) == Vector(3, 6)


def test_vector_unsupported_types():
    with pytest.raises(TypeError):
        Vector(1, 2) + 5
    with pytest.raises(TypeError):
        Vector(1, 2) * "x"


def test_vector_abs_and_bool():
    assert abs(Vector(3, 4)) == 5
    assert bool(Vector(0, 1))
    assert not Vector(0, 0)


def test_cart():
    c = Cart().add(Item("bread", 1.5, 2)).add(Item("milk", 0.99))
    assert c.total == 3.99
    assert len(c) == 3
    assert "bread" in c
    assert "wine" not in c
    assert [i.name for i in c] == ["bread", "milk"]
    assert c[1].name == "milk"


def test_empty_cart_is_falsy():
    assert not Cart()
    assert Cart().total == 0


def test_carts_dont_share_items():
    a, b = Cart(), Cart()
    a.add(Item("x", 1))
    assert len(b) == 0
