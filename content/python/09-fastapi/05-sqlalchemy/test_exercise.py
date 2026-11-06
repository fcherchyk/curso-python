import pytest
from exercise import Base, app, get_session
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client():
    """Each test uses a NEW in-memory database, injected with dependency_overrides."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    def override_session():
        with TestSession() as s:
            yield s

    app.dependency_overrides[get_session] = override_session
    yield TestClient(app)
    app.dependency_overrides.clear()


def create(client, title):
    return client.post("/tasks", json={"title": title})


def test_create(client):
    r = create(client, "buy mate")
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "buy mate", "done": False}


def test_create_validates(client):
    assert create(client, "").status_code == 422
    assert create(client, "x" * 101).status_code == 422
    assert client.post("/tasks", json={"title": "x", "id": 99}).json()["id"] == 1


def test_list_and_filter(client):
    for t in ["a", "b", "c"]:
        create(client, t)
    client.patch("/tasks/2", json={"done": True})
    assert [t["title"] for t in client.get("/tasks").json()] == ["a", "b", "c"]
    assert [t["title"] for t in client.get("/tasks", params={"done": True}).json()] == ["b"]
    assert [t["id"] for t in client.get("/tasks", params={"done": False}).json()] == [1, 3]


def test_detail(client):
    create(client, "a")
    assert client.get("/tasks/1").json()["title"] == "a"
    r = client.get("/tasks/9")
    assert r.status_code == 404
    assert r.json() == {"detail": "task not found"}


def test_partial_patch(client):
    create(client, "original")
    r = client.patch("/tasks/1", json={"done": True})
    assert r.status_code == 200
    assert r.json() == {"id": 1, "title": "original", "done": True}, "don't overwrite what wasn't sent"
    r = client.patch("/tasks/1", json={"title": "new"})
    assert r.json() == {"id": 1, "title": "new", "done": True}
    assert client.patch("/tasks/9", json={"done": True}).status_code == 404


def test_delete(client):
    create(client, "a")
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks").json() == []
    assert client.delete("/tasks/1").status_code == 404
