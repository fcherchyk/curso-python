import pytest
from exercise import Pila, activos, agrupar_por, primero


class TestPila:
    def test_operaciones(self):
        p = Pila()
        assert len(p) == 0
        assert not p
        assert p.tope() is None
        p.apilar(1)
        p.apilar(2)
        assert p
        assert p.tope() == 2
        assert p.desapilar() == 2
        assert p.desapilar() == 1
        with pytest.raises(IndexError):
            p.desapilar()

    def test_repr(self):
        assert repr(Pila([1, 2])) == "Pila([1, 2])"

    def test_es_generica_con_sintaxis_312(self):
        assert len(Pila.__type_params__) == 1
        Pila[int]()  # se puede parametrizar


def test_primero():
    assert primero([3, 4]) == 3
    assert primero(x for x in "abc") == "a"
    assert primero([]) is None
    assert primero([], default=0) == 0
    assert len(primero.__type_params__) == 1


def test_agrupar_por():
    assert agrupar_por(["ana", "beto", "abi"], lambda s: s[0]) == {
        "a": ["ana", "abi"],
        "b": ["beto"],
    }
    assert agrupar_por([1, 2, 3, 4], lambda n: n % 2 == 0) == {False: [1, 3], True: [2, 4]}
    assert len(agrupar_por.__type_params__) == 2


def test_activos():
    usuarios = [
        {"id": 3, "nombre": "caro", "activo": True},
        {"id": 1, "nombre": "ana", "activo": True},
        {"id": 2, "nombre": "beto", "activo": False},
    ]
    assert activos(usuarios) == ["ana", "caro"]
