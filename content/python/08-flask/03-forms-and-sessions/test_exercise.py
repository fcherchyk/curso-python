import exercise
import pytest
from exercise import app


@pytest.fixture
def cliente():
    exercise.TAREAS.clear()
    return app.test_client()


def test_lista_vacia(cliente):
    r = cliente.get("/tareas")
    assert r.status_code == 200
    assert "<ul></ul>" in r.text


def test_crear_redirige_con_flash(cliente):
    r = cliente.post("/tareas", data={"titulo": "  comprar yerba  "})
    assert r.status_code == 303
    assert r.headers["Location"].endswith("/tareas")
    r = cliente.get("/tareas")
    assert '<li id="t1">comprar yerba</li>' in r.text
    assert '<p class="flash">Tarea creada</p>' in r.text
    # el flash se consume una sola vez
    assert "Tarea creada" not in cliente.get("/tareas").text


def test_crear_invalido_muestra_errores(cliente):
    r = cliente.post("/tareas", data={"titulo": "   "})
    assert r.status_code == 400
    assert '<p class="error">El título es obligatorio</p>' in r.text
    r = cliente.post("/tareas", data={"titulo": "x" * 51})
    assert r.status_code == 400
    assert "Máximo 50 caracteres" in r.text
    assert 'value="' + "x" * 51 + '"' in r.text, "tiene que conservar lo que cargó el usuario"
    assert exercise.TAREAS == []


def test_borrar(cliente):
    cliente.post("/tareas", data={"titulo": "a"})
    cliente.post("/tareas", data={"titulo": "b"})
    r = cliente.post("/tareas/1/borrar", follow_redirects=True)
    assert r.status_code == 200
    assert 'id="t1"' not in r.text and 'id="t2"' in r.text
    assert "Tarea borrada" in r.text
    assert cliente.post("/tareas/99/borrar").status_code == 404


def test_preferencias_en_sesion(cliente):
    assert cliente.get("/preferencias").get_json() == {"tema": "claro"}
    assert cliente.post("/preferencias", data={"tema": "oscuro"}).status_code == 204
    assert cliente.get("/preferencias").get_json() == {"tema": "oscuro"}
    assert cliente.post("/preferencias", data={"tema": "rosa"}).status_code == 400
    otro = app.test_client()
    assert otro.get("/preferencias").get_json() == {"tema": "claro"}, "la sesión es por cliente"
