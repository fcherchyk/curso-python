import pytest
from ejercicio import RepoProductos, Usuario, app, get_repo, usuario_actual
from fastapi.testclient import TestClient

ANA = {"Authorization": "Bearer t-ana"}
BETO = {"Authorization": "Bearer t-beto"}


@pytest.fixture
def repo():
    """Repositorio falso, inyectado con dependency_overrides."""
    falso = RepoProductos(["a", "b", "c", "d", "e"])
    app.dependency_overrides[get_repo] = lambda: falso
    yield falso
    app.dependency_overrides.clear()


@pytest.fixture
def cliente(repo):
    return TestClient(app)


def test_paginacion(cliente):
    assert cliente.get("/productos").json() == ["a", "b", "c", "d", "e"]
    r = cliente.get("/productos", params={"pagina": 2, "por_pagina": 2})
    assert r.json() == ["c", "d"]


def test_paginacion_valida(cliente):
    assert cliente.get("/productos", params={"pagina": 0}).status_code == 422
    assert cliente.get("/productos", params={"por_pagina": 51}).status_code == 422


def test_yo(cliente):
    assert cliente.get("/yo", headers=BETO).json() == {"nombre": "beto", "es_admin": False}


def test_sin_token_o_invalido(cliente):
    r = cliente.get("/yo")
    assert r.status_code == 401
    assert r.json() == {"detail": "falta el token"}
    assert r.headers["WWW-Authenticate"] == "Bearer"
    r = cliente.get("/yo", headers={"Authorization": "Bearer nada"})
    assert r.status_code == 401
    assert r.json() == {"detail": "token inválido"}


def test_borrar_requiere_admin(cliente, repo):
    assert cliente.delete("/productos/0", headers=BETO).status_code == 403
    assert cliente.delete("/productos/0").status_code == 401
    assert cliente.delete("/productos/0", headers=ANA).status_code == 204
    assert repo.productos == ["b", "c", "d", "e"]
    assert cliente.delete("/productos/99", headers=ANA).status_code == 404


def test_override_del_usuario(cliente):
    app.dependency_overrides[usuario_actual] = lambda: Usuario("tester", es_admin=True)
    assert cliente.get("/yo").json() == {"nombre": "tester", "es_admin": True}
    assert cliente.delete("/productos/1").status_code == 204, "solo_admin depende de usuario_actual"
