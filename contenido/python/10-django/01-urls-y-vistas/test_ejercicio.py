import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="ejercicio",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
)
django.setup()

import copy

import ejercicio
import pytest
from django.test import Client
from django.urls import reverse

ORIGINAL = copy.deepcopy(ejercicio.PRODUCTOS)


@pytest.fixture
def cliente():
    ejercicio.PRODUCTOS.clear()
    ejercicio.PRODUCTOS.update(copy.deepcopy(ORIGINAL))
    return Client()


def test_inicio_y_saludo(cliente):
    assert cliente.get("/").content.decode() == "Hola, Django"
    assert cliente.get("/saludo/Ana/").content.decode() == "Hola, Ana!"


def test_listar(cliente):
    r = cliente.get("/productos/")
    assert r.status_code == 200
    assert [p["nombre"] for p in r.json()] == ["yerba", "café"]


def test_crear(cliente):
    r = cliente.post(
        "/productos/", data={"nombre": "té", "precio": 1200}, content_type="application/json"
    )
    assert r.status_code == 201
    assert r.json() == {"id": 3, "nombre": "té", "precio": 1200}
    r = cliente.post("/productos/", data={"nombre": "x"}, content_type="application/json")
    assert r.status_code == 400
    assert r.json() == {"error": "datos incompletos"}


def test_metodo_no_permitido(cliente):
    assert cliente.get("/productos/").status_code == 200
    assert cliente.delete("/productos/").status_code == 405


def test_detalle(cliente):
    assert cliente.get("/productos/2/").json()["nombre"] == "café"
    assert cliente.get("/productos/99/").status_code == 404
    assert cliente.get("/productos/abc/").status_code == 404


def test_urls_con_nombre():
    assert reverse("inicio") == "/"
    assert reverse("detalle", args=[3]) == "/productos/3/"
    assert reverse("saludo", kwargs={"nombre": "beto"}) == "/saludo/beto/"
