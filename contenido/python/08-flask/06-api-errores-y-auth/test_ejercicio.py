import pytest
from ejercicio import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True, "TOKENS": {"t-ana": "ana", "t-beto": "beto"}})


@pytest.fixture
def cliente(app):
    return app.test_client()


@pytest.fixture
def auth():
    return {"Authorization": "Bearer t-ana"}


def test_rutas_inexistentes_en_json(cliente):
    r = cliente.get("/no-existe")
    assert r.status_code == 404
    assert r.get_json()["error"] == "Not Found"
    r = cliente.delete("/api/notas")
    assert r.status_code == 405
    assert r.get_json()["error"] == "Method Not Allowed"


def test_yo_con_token(cliente, auth):
    r = cliente.get("/api/yo", headers=auth)
    assert r.status_code == 200
    assert r.get_json() == {"usuario": "ana"}


def test_sin_token(cliente):
    r = cliente.get("/api/yo")
    assert r.status_code == 401
    assert r.get_json() == {"error": "Unauthorized", "detalle": "falta el token"}
    r = cliente.get("/api/yo", headers={"Authorization": "Basic xxx"})
    assert r.get_json()["detalle"] == "falta el token"


def test_token_invalido(cliente):
    r = cliente.get("/api/yo", headers={"Authorization": "Bearer otro"})
    assert r.status_code == 401
    assert r.get_json()["detalle"] == "token inválido"


def test_crear_y_listar_notas(cliente, auth):
    r = cliente.post("/api/notas", json={"texto": "hola"}, headers=auth)
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "autor": "ana", "texto": "hola"}
    cliente.post("/api/notas", json={"texto": "chau"}, headers={"Authorization": "Bearer t-beto"})
    notas = cliente.get("/api/notas").get_json()
    assert [(n["autor"], n["texto"]) for n in notas] == [("ana", "hola"), ("beto", "chau")]


def test_crear_nota_invalida_y_sin_auth(cliente, auth):
    r = cliente.post("/api/notas", json={"texto": ""}, headers=auth)
    assert r.status_code == 400
    assert r.get_json() == {"error": "Bad Request", "detalle": "texto vacío"}
    assert cliente.post("/api/notas", json={"texto": "x"}).status_code == 401


def test_dos_vistas_protegidas_no_chocan(app):
    endpoints = {r.endpoint for r in app.url_map.iter_rules()}
    assert len([e for e in endpoints if e != "static"]) >= 3, "¿usaste functools.wraps?"
