import pytest
from exercise import STOCK_INICIAL, create_app
from fastapi.testclient import TestClient


@pytest.fixture
def cliente():
    with TestClient(create_app()) as c:  # el `with` ejecuta el lifespan
        yield c


def test_detalle_con_prefijos(cliente):
    r = cliente.get("/api/v1/productos/yerba")
    assert r.status_code == 200
    assert r.json() == {"nombre": "yerba", "stock": 10}


def test_vender(cliente):
    r = cliente.post("/api/v1/productos/yerba/ventas", json={"cantidad": 3})
    assert r.json() == {"nombre": "yerba", "stock": 7}
    assert cliente.get("/api/v1/productos/yerba").json()["stock"] == 7


def test_estado_por_app():
    with TestClient(create_app()) as a:
        a.post("/api/v1/productos/yerba/ventas", json={"cantidad": 5})
    with TestClient(create_app()) as b:
        assert b.get("/api/v1/productos/yerba").json()["stock"] == 10
    assert STOCK_INICIAL["yerba"] == 10, "no mutes STOCK_INICIAL: copialo en el lifespan"


def test_errores_de_dominio(cliente):
    r = cliente.get("/api/v1/productos/te")
    assert r.status_code == 404
    assert r.json() == {"error": "producto_no_encontrado", "nombre": "te"}
    r = cliente.post("/api/v1/productos/cafe/ventas", json={"cantidad": 5})
    assert r.status_code == 409
    assert r.json() == {"error": "stock_insuficiente", "disponible": 2}


def test_formato_de_validacion(cliente):
    r = cliente.post("/api/v1/productos/yerba/ventas", json={"cantidad": 0})
    assert r.status_code == 422
    assert r.json() == {"error": "validacion", "campos": ["cantidad"]}


def test_middleware_en_todas_las_respuestas(cliente):
    r = cliente.get("/api/v1/productos/yerba", headers={"X-Request-ID": "abc-123"})
    assert r.headers["X-Request-ID"] == "abc-123"
    assert float(r.headers["X-Tiempo-Proceso"]) >= 0
    r = cliente.get("/api/v1/productos/te")
    assert len(r.headers["X-Request-ID"]) == 32, "si no viene, generá uno con uuid4().hex"
