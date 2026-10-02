import copy

import ejercicio
import pytest
from ejercicio import app

ORIGINAL = copy.deepcopy(ejercicio.PRODUCTOS)


@pytest.fixture
def cliente():
    ejercicio.PRODUCTOS.clear()
    ejercicio.PRODUCTOS.update(copy.deepcopy(ORIGINAL))
    return app.test_client()


def test_inicio(cliente):
    r = cliente.get("/")
    assert r.status_code == 200
    assert r.text == "Hola, Flask!"


def test_saludo(cliente):
    assert cliente.get("/saludo/Ana").text == "Hola, Ana!"


def test_sumar(cliente):
    r = cliente.get("/sumar", query_string={"a": 2, "b": 40})
    assert r.status_code == 200
    assert r.get_json() == {"resultado": 42}


def test_sumar_invalido(cliente):
    for params in ({"a": 1}, {"a": "x", "b": 2}, {}):
        r = cliente.get("/sumar", query_string=params)
        assert r.status_code == 400, params
        assert r.get_json() == {"error": "a y b tienen que ser enteros"}


def test_detalle(cliente):
    r = cliente.get("/productos/2")
    assert r.status_code == 200
    assert r.get_json() == {"id": 2, "nombre": "café", "precio": 9800}


def test_detalle_inexistente(cliente):
    r = cliente.get("/productos/99")
    assert r.status_code == 404
    assert r.get_json() == {"error": "producto inexistente"}


def test_crear(cliente):
    r = cliente.post("/productos", json={"nombre": "té", "precio": 1200})
    assert r.status_code == 201
    assert r.get_json() == {"id": 3, "nombre": "té", "precio": 1200}
    assert cliente.get("/productos/3").status_code == 200


def test_crear_invalido(cliente):
    r = cliente.post("/productos", json={"nombre": "té"})
    assert r.status_code == 400
    assert r.get_json() == {"error": "nombre y precio son obligatorios"}
