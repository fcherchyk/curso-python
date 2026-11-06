import copy

import exercise
import pytest
from exercise import app
from fastapi.testclient import TestClient

ORIGINAL = copy.deepcopy(exercise.PRODUCTS)


@pytest.fixture
def client():
    exercise.PRODUCTS.clear()
    exercise.PRODUCTS.update(copy.deepcopy(ORIGINAL))
    return TestClient(app)


def test_home_and_greet(client):
    assert client.get("/").json() == {"message": "Hello, FastAPI"}
    assert client.get("/greet/Alice").json() == {"greeting": "Hello, Alice!"}


def test_add(client):
    r = client.get("/add", params={"a": 2, "b": 40})
    assert r.status_code == 200
    assert r.json() == {"result": 42}


def test_add_validates_automatically(client):
    assert client.get("/add", params={"a": 1}).status_code == 422
    assert client.get("/add", params={"a": "x", "b": 2}).status_code == 422


def test_list_with_filter(client):
    assert len(client.get("/products").json()) == 2
    cheap = client.get("/products", params={"max_price": 5000}).json()
    assert [p["name"] for p in cheap] == ["mate"]


def test_detail(client):
    assert client.get("/products/2").json() == {"id": 2, "name": "coffee", "price": 9800}
    r = client.get("/products/99")
    assert r.status_code == 404
    assert r.json() == {"detail": "product not found"}
    assert client.get("/products/abc").status_code == 422


def test_create(client):
    r = client.post("/products", json={"name": "tea", "price": 1200})
    assert r.status_code == 201
    assert r.json() == {"id": 3, "name": "tea", "price": 1200}
    assert client.post("/products", json={"name": "tea"}).status_code == 422


def test_docs_generated(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert {"/add", "/products", "/products/{id}"} <= set(paths)
