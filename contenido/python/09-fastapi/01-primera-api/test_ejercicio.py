import copy

import ejercicio
import pytest
from ejercicio import app
from fastapi.testclient import TestClient

ORIGINAL = copy.deepcopy(ejercicio.PRODUCTOS)


@pytest.fixture
def cliente():
    ejercicio.PRODUCTOS.clear()
    ejercicio.PRODUCTOS.update(copy.deepcopy(ORIGINAL))
    return TestClient(app)


def test_inicio_y_saludo(cliente):
    assert cliente.get("/").json() == {"mensaje": "Hola, FastAPI"}
    assert cliente.get("/saludo/Ana").json() == {"saludo": "Hola, Ana!"}


def test_sumar(cliente):
    r = cliente.get("/sumar", params={"a": 2, "b": 40})
    assert r.status_code == 200
    assert r.json() == {"resultado": 42}


def test_sumar_valida_automaticamente(cliente):
    assert cliente.get("/sumar", params={"a": 1}).status_code == 422
    assert cliente.get("/sumar", params={"a": "x", "b": 2}).status_code == 422


def test_listar_con_filtro(cliente):
    assert len(cliente.get("/productos").json()) == 2
    baratos = cliente.get("/productos", params={"max_precio": 5000}).json()
    assert [p["nombre"] for p in baratos] == ["yerba"]


def test_detalle(cliente):
    assert cliente.get("/productos/2").json() == {"id": 2, "nombre": "café", "precio": 9800}
    r = cliente.get("/productos/99")
    assert r.status_code == 404
    assert r.json() == {"detail": "producto inexistente"}
    assert cliente.get("/productos/abc").status_code == 422


def test_crear(cliente):
    r = cliente.post("/productos", json={"nombre": "té", "precio": 1200})
    assert r.status_code == 201
    assert r.json() == {"id": 3, "nombre": "té", "precio": 1200}
    assert cliente.post("/productos", json={"nombre": "té"}).status_code == 422


def test_documentacion_generada(cliente):
    rutas = cliente.get("/openapi.json").json()["paths"]
    assert {"/sumar", "/productos", "/productos/{id}"} <= set(rutas)
