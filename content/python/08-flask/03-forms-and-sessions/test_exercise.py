import exercise
import pytest
from exercise import app


@pytest.fixture
def client():
    exercise.TASKS.clear()
    return app.test_client()


def test_empty_list(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert "<ul></ul>" in r.text


def test_create_redirects_with_flash(client):
    r = client.post("/tasks", data={"title": "  buy coffee  "})
    assert r.status_code == 303
    assert r.headers["Location"].endswith("/tasks")
    r = client.get("/tasks")
    assert '<li id="t1">buy coffee</li>' in r.text
    assert '<p class="flash">Task created</p>' in r.text
    # the flash is consumed only once
    assert "Task created" not in client.get("/tasks").text


def test_create_invalid_shows_errors(client):
    r = client.post("/tasks", data={"title": "   "})
    assert r.status_code == 400
    assert '<p class="error">Title is required</p>' in r.text
    r = client.post("/tasks", data={"title": "x" * 51})
    assert r.status_code == 400
    assert "50 characters max" in r.text
    assert 'value="' + "x" * 51 + '"' in r.text, "it must keep what the user typed"
    assert exercise.TASKS == []


def test_delete(client):
    client.post("/tasks", data={"title": "a"})
    client.post("/tasks", data={"title": "b"})
    r = client.post("/tasks/1/delete", follow_redirects=True)
    assert r.status_code == 200
    assert 'id="t1"' not in r.text and 'id="t2"' in r.text
    assert "Task deleted" in r.text
    assert client.post("/tasks/99/delete").status_code == 404


def test_preferences_in_session(client):
    assert client.get("/preferences").get_json() == {"theme": "light"}
    assert client.post("/preferences", data={"theme": "dark"}).status_code == 204
    assert client.get("/preferences").get_json() == {"theme": "dark"}
    assert client.post("/preferences", data={"theme": "pink"}).status_code == 400
    other = app.test_client()
    assert other.get("/preferences").get_json() == {"theme": "light"}, "the session is per client"
