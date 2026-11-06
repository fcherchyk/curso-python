import pytest
from exercise import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_status_in_api_blueprint(client):
    r = client.get("/api/status")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok", "environment": "development"}
    assert client.get("/status").status_code == 404, "it must live under /api"


def test_web_uses_config(client):
    assert client.get("/").text == "Hello, visitor"


def test_config_overrides_defaults():
    app = create_app({"ENVIRONMENT": "test", "GREETING": "Hi"})
    c = app.test_client()
    assert c.get("/api/status").get_json()["environment"] == "test"
    assert c.get("/").text == "Hi, visitor"
    assert app.config["SECRET_KEY"] == "dev"


def test_independent_apps():
    a = create_app({"GREETING": "A"})
    b = create_app({"GREETING": "B"})
    assert a.test_client().get("/").text == "A, visitor"
    assert b.test_client().get("/").text == "B, visitor"


def test_url_for_with_blueprint(client):
    r = client.get("/go-to-status")
    assert r.status_code == 302
    assert r.headers["Location"] == "/api/status"


def test_extension_counts_per_app():
    app = create_app()
    c = app.test_client()
    c.get("/")
    c.get("/api/status")
    assert c.get("/api/visits").get_json() == {"visits": 3}
    other = create_app().test_client()
    assert other.get("/api/visits").get_json() == {"visits": 1}, "the state is per app"
