import io
import math

import pytest
from ejercicio import Circulo, Notificador, NotificadorMemoria, area_total, cerrar_todos


def test_area_total_duck_typing():
    class Cuadrado:  # no hereda de nada
        def area(self):
            return 4.0

    assert area_total([Circulo(1), Cuadrado()]) == pytest.approx(math.pi + 4)
    assert area_total([]) == 0


def test_notificador_es_abstracto():
    with pytest.raises(TypeError):
        Notificador()


def test_subclase_incompleta_no_se_instancia():
    class Incompleto(Notificador):
        pass

    with pytest.raises(TypeError):
        Incompleto()


def test_notificador_memoria():
    n = NotificadorMemoria()
    assert n.enviar("ana", "hola") is True
    assert n.enviar("", "hola") is False
    assert n.enviados == [("ana", "hola")]


def test_enviar_a_todos_usa_enviar():
    n = NotificadorMemoria()
    assert n.enviar_a_todos(["a", "", "b"], "x") == 2
    assert n.enviados == [("a", "x"), ("b", "x")]


def test_cerrar_todos():
    archivo = io.StringIO("x")

    class Conexion:
        def __init__(self):
            self.cerrada = False

        def close(self):
            self.cerrada = True

    c = Conexion()
    assert cerrar_todos([archivo, c, 42, "texto"]) == 2
    assert archivo.closed and c.cerrada
