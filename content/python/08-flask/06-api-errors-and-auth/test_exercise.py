import pytest
from exercise import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True, "TOKENS": {"t-alice": "alice", "t-bob": "bob"}})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth():
    return {"Authorization": "Bearer t-alice"}


def test_unknown_routes_in_json(client):
    r = client.get("/does-not-exist")
    assert r.status_code == 404
    assert r.get_json()["error"] == "Not Found"
    r = client.delete("/api/notes")
    assert r.status_code == 405
    assert r.get_json()["error"] == "Method Not Allowed"


def test_me_with_token(client, auth):
    r = client.get("/api/me", headers=auth)
    assert r.status_code == 200
    assert r.get_json() == {"user": "alice"}


def test_no_token(client):
    r = client.get("/api/me")
    assert r.status_code == 401
    assert r.get_json() == {"error": "Unauthorized", "detail": "missing token"}
    r = client.get("/api/me", headers={"Authorization": "Basic xxx"})
    assert r.get_json()["detail"] == "missing token"


def test_invalid_token(client):
    r = client.get("/api/me", headers={"Authorization": "Bearer other"})
    assert r.status_code == 401
    assert r.get_json()["detail"] == "invalid token"


def test_create_and_list_notes(client, auth):
    r = client.post("/api/notes", json={"text": "hello"}, headers=auth)
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "author": "alice", "text": "hello"}
    client.post("/api/notes", json={"text": "bye"}, headers={"Authorization": "Bearer t-bob"})
    notes = client.get("/api/notes").get_json()
    assert [(n["author"], n["text"]) for n in notes] == [("alice", "hello"), ("bob", "bye")]


def test_create_invalid_note_and_no_auth(client, auth):
    r = client.post("/api/notes", json={"text": ""}, headers=auth)
    assert r.status_code == 400
    assert r.get_json() == {"error": "Bad Request", "detail": "empty text"}
    assert client.post("/api/notes", json={"text": "x"}).status_code == 401


def test_two_protected_views_dont_clash(app):
    endpoints = {r.endpoint for r in app.url_map.iter_rules()}
    assert len([e for e in endpoints if e != "static"]) >= 3, "did you use functools.wraps?"
