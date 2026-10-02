import re

import pytest
from ejercicio import app


@pytest.fixture
def cliente():
    return app.test_client()


def nombres_listados(html: str) -> list[str]:
    return re.findall(r'<a href="/productos/\d+">([^<]+)</a>', html)


def test_filtro_pesos():
    filtro = app.jinja_env.filters.get("pesos")
    assert filtro is not None, "registrá el filtro con @app.template_filter('pesos')"
    assert filtro(3500) == "$ 3.500,00"
    assert filtro(1234567.5) == "$ 1.234.567,50"


def test_lista(cliente):
    r = cliente.get("/productos")
    assert r.status_code == 200
    assert "<h1>Productos (3)</h1>" in r.text
    assert nombres_listados(r.text) == ["azúcar", "café", "yerba"]
    assert "$ 9.800,00" in r.text
    assert "<title>Productos</title>" in r.text, "tiene que heredar de base.html"


def test_lista_filtrada(cliente):
    r = cliente.get("/productos", query_string={"max": 4000})
    assert nombres_listados(r.text) == ["azúcar", "yerba"]
    r = cliente.get("/productos", query_string={"max": 10})
    assert "No hay productos" in r.text


def test_detalle(cliente):
    r = cliente.get("/productos/2")
    assert r.status_code == 200
    assert "<h1>café</h1>" in r.text
    assert "Producto premium" in r.text
    assert "Producto premium" not in cliente.get("/productos/1").text
    assert cliente.get("/productos/99").status_code == 404


def test_saludo_escapa_html(cliente):
    r = cliente.get("/saludo/<img src=x onerror=alert(1)>")
    assert r.status_code == 200
    assert "&lt;img" in r.text
    assert "<img" not in r.text
    assert cliente.get("/saludo/Ana").text == "<p>Hola, Ana!</p>"
