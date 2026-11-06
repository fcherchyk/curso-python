import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="exercise",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth", "rest_framework"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    REST_FRAMEWORK={"UNAUTHENTICATED_USER": None},
    USE_TZ=True,
)
django.setup()

import pytest
from django.db import connection
from exercise import Tarea
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def tablas():
    with connection.schema_editor() as editor:
        editor.create_model(Tarea)
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Tarea)


@pytest.fixture
def api():
    return APIClient()


def crear(api, titulo):
    return api.post("/api/tareas/", {"titulo": titulo}, format="json")


def test_crear(api):
    r = crear(api, "  comprar yerba ")
    assert r.status_code == 201
    datos = r.json()
    assert datos["titulo"] == "comprar yerba"
    assert datos["hecha"] is False
    assert {"id", "creada"} <= set(datos)


def test_validacion(api):
    r = crear(api, " ToDo ")
    assert r.status_code == 400
    assert r.json() == {"titulo": ["Poné un título descriptivo"]}
    r = api.post("/api/tareas/", {"titulo": "x", "id": 99, "creada": "2000-01-01"}, format="json")
    assert r.json()["id"] != 99, "id es de solo lectura"


def test_listar_detalle_y_borrar(api):
    for t in ["a", "b"]:
        crear(api, t)
    assert [t["titulo"] for t in api.get("/api/tareas/").json()] == ["a", "b"]
    id_b = api.get("/api/tareas/").json()[1]["id"]
    assert api.get(f"/api/tareas/{id_b}/").json()["titulo"] == "b"
    assert api.patch(f"/api/tareas/{id_b}/", {"hecha": True}, format="json").json()["hecha"]
    assert api.delete(f"/api/tareas/{id_b}/").status_code == 204
    assert api.get(f"/api/tareas/{id_b}/").status_code == 404


def test_filtro_y_accion_completar(api):
    ids = [crear(api, t).json()["id"] for t in ["a", "b", "c"]]
    r = api.post(f"/api/tareas/{ids[1]}/completar/")
    assert r.status_code == 200
    assert r.json()["hecha"] is True
    assert [t["titulo"] for t in api.get("/api/tareas/", {"hecha": "true"}).json()] == ["b"]
    assert [t["titulo"] for t in api.get("/api/tareas/", {"hecha": "false"}).json()] == ["a", "c"]
    assert api.post("/api/tareas/999/completar/").status_code == 404


def test_estadisticas(api):
    ids = [crear(api, t).json()["id"] for t in ["a", "b", "c"]]
    api.post(f"/api/tareas/{ids[0]}/completar/")
    r = api.get("/api/estadisticas/")
    assert r.status_code == 200
    assert r.json() == {"total": 3, "hechas": 1, "pendientes": 2}
