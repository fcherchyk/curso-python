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
from exercise import Task
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def tables():
    with connection.schema_editor() as editor:
        editor.create_model(Task)
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Task)


@pytest.fixture
def api():
    return APIClient()


def create(api, title):
    return api.post("/api/tasks/", {"title": title}, format="json")


def test_create(api):
    r = create(api, "  buy mate ")
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "buy mate"
    assert data["done"] is False
    assert {"id", "created"} <= set(data)


def test_validation(api):
    r = create(api, " ToDo ")
    assert r.status_code == 400
    assert r.json() == {"title": ["Use a descriptive title"]}
    r = api.post("/api/tasks/", {"title": "x", "id": 99, "created": "2000-01-01"}, format="json")
    assert r.json()["id"] != 99, "id is read-only"


def test_list_detail_and_delete(api):
    for t in ["a", "b"]:
        create(api, t)
    assert [t["title"] for t in api.get("/api/tasks/").json()] == ["a", "b"]
    id_b = api.get("/api/tasks/").json()[1]["id"]
    assert api.get(f"/api/tasks/{id_b}/").json()["title"] == "b"
    assert api.patch(f"/api/tasks/{id_b}/", {"done": True}, format="json").json()["done"]
    assert api.delete(f"/api/tasks/{id_b}/").status_code == 204
    assert api.get(f"/api/tasks/{id_b}/").status_code == 404


def test_filter_and_complete_action(api):
    ids = [create(api, t).json()["id"] for t in ["a", "b", "c"]]
    r = api.post(f"/api/tasks/{ids[1]}/complete/")
    assert r.status_code == 200
    assert r.json()["done"] is True
    assert [t["title"] for t in api.get("/api/tasks/", {"done": "true"}).json()] == ["b"]
    assert [t["title"] for t in api.get("/api/tasks/", {"done": "false"}).json()] == ["a", "c"]
    assert api.post("/api/tasks/999/complete/").status_code == 404


def test_stats(api):
    ids = [create(api, t).json()["id"] for t in ["a", "b", "c"]]
    api.post(f"/api/tasks/{ids[0]}/complete/")
    r = api.get("/api/stats/")
    assert r.status_code == 200
    assert r.json() == {"total": 3, "done": 1, "pending": 2}
