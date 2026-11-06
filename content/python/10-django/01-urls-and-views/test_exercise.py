import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="exercise",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
)
django.setup()

import copy

import exercise
import pytest
from django.test import Client
from django.urls import reverse

ORIGINAL = copy.deepcopy(exercise.PRODUCTS)


@pytest.fixture
def client():
    exercise.PRODUCTS.clear()
    exercise.PRODUCTS.update(copy.deepcopy(ORIGINAL))
    return Client()


def test_home_and_greet(client):
    assert client.get("/").content.decode() == "Hello, Django"
    assert client.get("/greet/Alice/").content.decode() == "Hello, Alice!"


def test_list(client):
    r = client.get("/products/")
    assert r.status_code == 200
    assert [p["name"] for p in r.json()] == ["mate", "coffee"]


def test_create(client):
    r = client.post(
        "/products/", data={"name": "tea", "price": 1200}, content_type="application/json"
    )
    assert r.status_code == 201
    assert r.json() == {"id": 3, "name": "tea", "price": 1200}
    r = client.post("/products/", data={"name": "x"}, content_type="application/json")
    assert r.status_code == 400
    assert r.json() == {"error": "incomplete data"}


def test_method_not_allowed(client):
    assert client.get("/products/").status_code == 200
    assert client.delete("/products/").status_code == 405


def test_detail(client):
    assert client.get("/products/2/").json()["name"] == "coffee"
    assert client.get("/products/99/").status_code == 404
    assert client.get("/products/abc/").status_code == 404


def test_named_urls():
    assert reverse("home") == "/"
    assert reverse("detail", args=[3]) == "/products/3/"
    assert reverse("greet", kwargs={"name": "bob"}) == "/greet/bob/"
