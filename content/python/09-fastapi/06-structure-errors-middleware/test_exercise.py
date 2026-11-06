import pytest
from exercise import INITIAL_STOCK, create_app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with TestClient(create_app()) as c:  # the `with` runs the lifespan
        yield c


def test_detail_with_prefixes(client):
    r = client.get("/api/v1/products/mate")
    assert r.status_code == 200
    assert r.json() == {"name": "mate", "stock": 10}


def test_sell(client):
    r = client.post("/api/v1/products/mate/sales", json={"quantity": 3})
    assert r.json() == {"name": "mate", "stock": 7}
    assert client.get("/api/v1/products/mate").json()["stock"] == 7


def test_state_per_app():
    with TestClient(create_app()) as a:
        a.post("/api/v1/products/mate/sales", json={"quantity": 5})
    with TestClient(create_app()) as b:
        assert b.get("/api/v1/products/mate").json()["stock"] == 10
    assert INITIAL_STOCK["mate"] == 10, "don't mutate INITIAL_STOCK: copy it in the lifespan"


def test_domain_errors(client):
    r = client.get("/api/v1/products/tea")
    assert r.status_code == 404
    assert r.json() == {"error": "product_not_found", "name": "tea"}
    r = client.post("/api/v1/products/coffee/sales", json={"quantity": 5})
    assert r.status_code == 409
    assert r.json() == {"error": "insufficient_stock", "available": 2}


def test_validation_format(client):
    r = client.post("/api/v1/products/mate/sales", json={"quantity": 0})
    assert r.status_code == 422
    assert r.json() == {"error": "validation", "fields": ["quantity"]}


def test_middleware_on_every_response(client):
    r = client.get("/api/v1/products/mate", headers={"X-Request-ID": "abc-123"})
    assert r.headers["X-Request-ID"] == "abc-123"
    assert float(r.headers["X-Process-Time"]) >= 0
    r = client.get("/api/v1/products/tea")
    assert len(r.headers["X-Request-ID"]) == 32, "if none is sent, generate one with uuid4().hex"
