import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="ejercicio",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "django.contrib.sessions",
        "django.contrib.messages",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
            "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
        }
    ],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
)
django.setup()

import re

import pytest
from django.contrib import admin
from django.db import connection
from django.test import Client
from ejercicio import Libro

LIBROS = [
    ("Rayuela", "Cortázar", 1963),
    ("Ficciones", "Borges", 1944),
    ("El túnel", "Sabato", 1948),
    ("Bestiario", "Cortázar", 1951),
    ("El Aleph", "Borges", 1949),
]


@pytest.fixture(autouse=True)
def datos():
    with connection.schema_editor() as editor:
        editor.create_model(Libro)
    for titulo, autor, anio in LIBROS:
        Libro.objects.create(titulo=titulo, autor=autor, anio=anio)
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Libro)


def titulos(html: str) -> list[str]:
    return re.findall(r'<a href="/libros/\d+/">([^<]+)</a>', html)


def test_lista_ordenada_y_paginada():
    c = Client()
    html = c.get("/libros/").content.decode()
    assert titulos(html) == ["Bestiario", "El Aleph", "El túnel"]
    assert "Página 1 de 2" in html
    assert titulos(c.get("/libros/", {"page": 2}).content.decode()) == ["Ficciones", "Rayuela"]


def test_lista_con_busqueda():
    html = Client().get("/libros/", {"q": "EL "}).content.decode()
    assert titulos(html) == ["El Aleph", "El túnel"]
    html = Client().get("/libros/", {"q": "zzz"}).content.decode()
    assert "No hay libros" in html


def test_detalle():
    libro = Libro.objects.get(titulo="Ficciones")
    html = Client().get(f"/libros/{libro.pk}/").content.decode()
    assert "<h1>Ficciones</h1>" in html and "Borges" in html
    assert Client().get("/libros/999/").status_code == 404


def test_crear_valida_y_redirige():
    c = Client()
    assert c.get("/libros/nuevo/").status_code == 200
    r = c.post("/libros/nuevo/", {"titulo": "Zama", "autor": "Di Benedetto", "anio": 1956})
    assert r.status_code == 302
    assert r.headers["Location"] == "/libros/"
    assert Libro.objects.filter(titulo="Zama").exists()
    r = c.post("/libros/nuevo/", {"titulo": "", "autor": "X", "anio": "no"})
    assert r.status_code == 200, "con errores re-renderiza el formulario"
    assert Libro.objects.count() == 6


def test_admin_registrado():
    assert admin.site.is_registered(Libro)
    modelo_admin = admin.site._registry[Libro]
    assert list(modelo_admin.list_display) == ["titulo", "autor", "anio"]
    assert list(modelo_admin.search_fields) == ["titulo", "autor"]
    assert list(modelo_admin.list_filter) == ["anio"]
