import re

import pytest
from exercise import app


@pytest.fixture
def client():
    return app.test_client()


def listed_names(html: str) -> list[str]:
    return re.findall(r'<a href="/products/\d+">([^<]+)</a>', html)


def test_money_filter():
    money_filter = app.jinja_env.filters.get("money")
    assert money_filter is not None, "register the filter with @app.template_filter('money')"
    assert money_filter(3500) == "$ 3.500,00"
    assert money_filter(1234567.5) == "$ 1.234.567,50"


def test_list(client):
    r = client.get("/products")
    assert r.status_code == 200
    assert "<h1>Products (3)</h1>" in r.text
    assert listed_names(r.text) == ["coffee", "sugar", "tea"]
    assert "$ 9.800,00" in r.text
    assert "<title>Products</title>" in r.text, "it must extend base.html"


def test_filtered_list(client):
    r = client.get("/products", query_string={"max": 4000})
    assert listed_names(r.text) == ["sugar", "tea"]
    r = client.get("/products", query_string={"max": 10})
    assert "No products" in r.text


def test_detail(client):
    r = client.get("/products/2")
    assert r.status_code == 200
    assert "<h1>coffee</h1>" in r.text
    assert "Premium product" in r.text
    assert "Premium product" not in client.get("/products/1").text
    assert client.get("/products/99").status_code == 404


def test_greet_escapes_html(client):
    r = client.get("/greet/<img src=x onerror=alert(1)>")
    assert r.status_code == 200
    assert "&lt;img" in r.text
    assert "<img" not in r.text
    assert client.get("/greet/Alice").text == "<p>Hello, Alice!</p>"
