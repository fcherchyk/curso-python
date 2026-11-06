import copy

import exercise
import pytest
from exercise import app

ORIGINAL = copy.deepcopy(exercise.PRODUCTS)


@pytest.fixture
def client():
    exercise.PRODUCTS.clear()
    exercise.PRODUCTS.update(copy.deepcopy(ORIGINAL))
    return app.test_client()


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.text == "Hello, Flask!"


def test_greet(client):
    assert client.get("/greet/Alice").text == "Hello, Alice!"


def test_add(client):
    r = client.get("/add", query_string={"a": 2, "b": 40})
    assert r.status_code == 200
    assert r.get_json() == {"result": 42}


def test_add_invalid(client):
    for params in ({"a": 1}, {"a": "x", "b": 2}, {}):
        r = client.get("/add", query_string=params)
        assert r.status_code == 400, params
        assert r.get_json() == {"error": "a and b must be integers"}


def test_detail(client):
    r = client.get("/products/2")
    assert r.status_code == 200
    assert r.get_json() == {"id": 2, "name": "coffee", "price": 9800}


def test_detail_not_found(client):
    r = client.get("/products/99")
    assert r.status_code == 404
    assert r.get_json() == {"error": "product not found"}


def test_create(client):
    r = client.post("/products", json={"name": "juice", "price": 1200})
    assert r.status_code == 201
    assert r.get_json() == {"id": 3, "name": "juice", "price": 1200}
    assert client.get("/products/3").status_code == 200


def test_create_invalid(client):
    r = client.post("/products", json={"name": "juice"})
    assert r.status_code == 400
    assert r.get_json() == {"error": "name and price are required"}
