import dataclasses

import pytest
from exercise import Pedido, Punto, Version


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


class TestPedido:
    def test_defaults_independientes(self):
        a, b = Pedido("ana"), Pedido("beto")
        a.items.append("yerba")
        assert b.items == []
        assert a.estado == "nuevo"

    def test_valida_cliente(self):
        with pytest.raises(ValueError):
            Pedido("   ")

    def test_con_estado_no_muta(self):
        p = Pedido("ana", ["pan"])
        q = p.con_estado("enviado")
        assert q.estado == "enviado"
        assert p.estado == "nuevo"
        assert q.items == ["pan"]

    def test_a_dict(self):
        assert Pedido("ana", ["pan"]).a_dict() == {
            "cliente": "ana",
            "items": ["pan"],
            "estado": "nuevo",
        }

    def test_es_dataclass(self):
        assert dataclasses.is_dataclass(Pedido)
