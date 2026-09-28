import dataclasses
import math

import pytest

from semana1.dia4_modelado.ejercicios import (
    Carrito,
    Circulo,
    Estado,
    Item,
    Pila,
    Punto,
    Rectangulo,
    Version,
    area_total,
    primero,
)


class TestPunto:
    def test_distancia(self):
        assert Punto(0, 0).distancia(Punto(3, 4)) == 5

    def test_suma(self):
        assert Punto(1, 2) + Punto(3, 4) == Punto(4, 6)

    def test_inmutable_y_hasheable(self):
        p = Punto(1, 1)
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.x = 5
        assert len({Punto(1, 1), Punto(1, 1), Punto(2, 2)}) == 2


class TestVersion:
    def test_desde_str(self):
        assert Version.desde_str("1.2.3") == Version(1, 2, 3)
        assert Version.desde_str("2") == Version(2, 0, 0)
        with pytest.raises(ValueError):
            Version.desde_str("1.x")

    def test_orden(self):
        vs = [Version.desde_str(s) for s in ["1.10.0", "1.2.0", "0.9.9", "1.2.10"]]
        assert [str(v) for v in sorted(vs)] == ["0.9.9", "1.2.0", "1.2.10", "1.10.0"]
        assert Version(2) > Version(1, 99, 99)

    def test_str_y_repr(self):
        v = Version(1, 2, 3)
        assert str(v) == "1.2.3"
        assert repr(v) == "Version(mayor=1, menor=2, parche=3)"


class TestEstado:
    def test_es_string(self):
        assert Estado.PENDIENTE == "pendiente"
        assert Estado("en_curso") is Estado.EN_CURSO

    def test_siguiente(self):
        assert Estado.PENDIENTE.siguiente() is Estado.EN_CURSO
        assert Estado.EN_CURSO.siguiente() is Estado.TERMINADO
        with pytest.raises(ValueError):
            Estado.TERMINADO.siguiente()


class TestCarrito:
    def test_carrito(self):
        c = Carrito().agregar(Item("pan", 1.5, 2)).agregar(Item("leche", 0.99))
        assert c.total == 3.99
        assert len(c) == 3
        assert "pan" in c
        assert "vino" not in c
        assert [i.nombre for i in c] == ["pan", "leche"]

    def test_no_comparten_lista(self):
        a, b = Carrito(), Carrito()
        a.agregar(Item("x", 1))
        assert len(b) == 0


class TestFiguras:
    def test_area_total_duck_typing(self):
        class Cuadrado:  # no hereda de nada
            def area(self):
                return 4.0

        total = area_total([Circulo(1), Rectangulo(2, 3), Cuadrado()])
        assert total == pytest.approx(math.pi + 6 + 4)

    def test_rectangulo_valida(self):
        with pytest.raises(ValueError):
            Rectangulo(-1, 2)


class TestPila:
    def test_operaciones(self):
        p: Pila[int] = Pila()
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


def test_primero():
    assert primero([3, 4]) == 3
    assert primero(x for x in "abc") == "a"
    assert primero([]) is None
    assert primero([], default=0) == 0
