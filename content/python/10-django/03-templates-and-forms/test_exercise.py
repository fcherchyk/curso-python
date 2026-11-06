import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="exercise",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
    MIDDLEWARE=["django.middleware.csrf.CsrfViewMiddleware"],
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": ["templates"]}],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
)
django.setup()

import re

import exercise
import pytest
from django.test import Client
from exercise import ContactoForm

VALIDO = {"nombre": "  ana pérez ", "email": "ana@x.com", "mensaje": "Hola, quiero info"}


@pytest.fixture(autouse=True)
def limpiar():
    exercise.MENSAJES.clear()


def test_form_valido_limpia_el_nombre():
    form = ContactoForm(data=VALIDO)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["nombre"] == "Ana Pérez"


def test_form_errores_por_campo():
    form = ContactoForm(data={"nombre": "x" * 51, "email": "no-es-email", "mensaje": "corto"})
    assert not form.is_valid()
    assert set(form.errors) == {"nombre", "email", "mensaje"}


def test_form_regla_general():
    form = ContactoForm(data=VALIDO | {"mensaje": "Compre SPAM barato ya"})
    assert not form.is_valid()
    assert form.non_field_errors() == ["El mensaje parece spam"]


def test_get_muestra_el_form():
    r = Client().get("/contacto/")
    assert r.status_code == 200
    html = r.content.decode()
    assert "<title>Contacto</title>" in html
    assert 'name="email"' in html and "csrfmiddlewaretoken" in html


def test_post_valido_redirige_y_agradece():
    c = Client()
    r = c.post("/contacto/", VALIDO)
    assert r.status_code == 302
    assert r.headers["Location"] == "/gracias/"
    assert exercise.MENSAJES[0]["nombre"] == "Ana Pérez"
    html = c.get("/gracias/").content.decode()
    assert "¡Gracias, Ana Pérez!" in html
    assert "Recibimos 1 mensaje." in html


def test_post_invalido_muestra_errores():
    r = Client().post("/contacto/", VALIDO | {"email": "malo"})
    assert r.status_code == 200
    assert 'data-campo="email"' in r.content.decode()
    assert exercise.MENSAJES == []


def test_csrf():
    c = Client(enforce_csrf_checks=True)
    assert c.post("/contacto/", VALIDO).status_code == 403
    token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', c.get("/contacto/").content.decode())
    assert token, "la plantilla tiene {% csrf_token %}: renderizá con render(request, ...)"
    r = c.post("/contacto/", VALIDO | {"csrfmiddlewaretoken": token.group(1)})
    assert r.status_code == 302
