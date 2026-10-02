import pytest
from ejercicio import Base, app, get_session
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def cliente():
    """Cada test usa una base en memoria NUEVA, inyectada con dependency_overrides."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    Sesion = sessionmaker(bind=engine)

    def sesion_de_test():
        with Sesion() as s:
            yield s

    app.dependency_overrides[get_session] = sesion_de_test
    yield TestClient(app)
    app.dependency_overrides.clear()


def crear(cliente, titulo):
    return cliente.post("/tareas", json={"titulo": titulo})


def test_crear(cliente):
    r = crear(cliente, "comprar yerba")
    assert r.status_code == 201
    assert r.json() == {"id": 1, "titulo": "comprar yerba", "hecha": False}


def test_crear_valida(cliente):
    assert crear(cliente, "").status_code == 422
    assert crear(cliente, "x" * 101).status_code == 422
    assert cliente.post("/tareas", json={"titulo": "x", "id": 99}).json()["id"] == 1


def test_listar_y_filtrar(cliente):
    for t in ["a", "b", "c"]:
        crear(cliente, t)
    cliente.patch("/tareas/2", json={"hecha": True})
    assert [t["titulo"] for t in cliente.get("/tareas").json()] == ["a", "b", "c"]
    assert [t["titulo"] for t in cliente.get("/tareas", params={"hecha": True}).json()] == ["b"]
    assert [t["id"] for t in cliente.get("/tareas", params={"hecha": False}).json()] == [1, 3]


def test_detalle(cliente):
    crear(cliente, "a")
    assert cliente.get("/tareas/1").json()["titulo"] == "a"
    r = cliente.get("/tareas/9")
    assert r.status_code == 404
    assert r.json() == {"detail": "tarea inexistente"}


def test_patch_parcial(cliente):
    crear(cliente, "original")
    r = cliente.patch("/tareas/1", json={"hecha": True})
    assert r.status_code == 200
    assert r.json() == {"id": 1, "titulo": "original", "hecha": True}, "no pises lo que no vino"
    r = cliente.patch("/tareas/1", json={"titulo": "nuevo"})
    assert r.json() == {"id": 1, "titulo": "nuevo", "hecha": True}
    assert cliente.patch("/tareas/9", json={"hecha": True}).status_code == 404


def test_borrar(cliente):
    crear(cliente, "a")
    assert cliente.delete("/tareas/1").status_code == 204
    assert cliente.get("/tareas").json() == []
    assert cliente.delete("/tareas/1").status_code == 404
