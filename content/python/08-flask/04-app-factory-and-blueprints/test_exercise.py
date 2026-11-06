import pytest
from exercise import create_app


@pytest.fixture
def cliente():
    return create_app().test_client()


def test_estado_en_blueprint_api(cliente):
    r = cliente.get("/api/estado")
    assert r.status_code == 200
    assert r.get_json() == {"estado": "ok", "entorno": "desarrollo"}
    assert cliente.get("/estado").status_code == 404, "tiene que estar bajo /api"


def test_web_usa_la_config(cliente):
    assert cliente.get("/").text == "Hola, visitante"


def test_config_pisa_los_defaults():
    app = create_app({"ENTORNO": "test", "SALUDO": "Buenas"})
    c = app.test_client()
    assert c.get("/api/estado").get_json()["entorno"] == "test"
    assert c.get("/").text == "Buenas, visitante"
    assert app.config["SECRET_KEY"] == "dev"


def test_apps_independientes():
    a = create_app({"SALUDO": "A"})
    b = create_app({"SALUDO": "B"})
    assert a.test_client().get("/").text == "A, visitante"
    assert b.test_client().get("/").text == "B, visitante"


def test_url_for_con_blueprint(cliente):
    r = cliente.get("/ir-al-estado")
    assert r.status_code == 302
    assert r.headers["Location"] == "/api/estado"


def test_extension_cuenta_por_app():
    app = create_app()
    c = app.test_client()
    c.get("/")
    c.get("/api/estado")
    assert c.get("/api/visitas").get_json() == {"visitas": 3}
    otra = create_app().test_client()
    assert otra.get("/api/visitas").get_json() == {"visitas": 1}, "el estado va por app"
