import pytest
from exercise import Autor, create_app, db, obtener_o_crear_autor
from sqlalchemy import func, select


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def cliente(app):
    return app.test_client()


def cargar(cliente):
    for titulo, autor, anio in [
        ("Rayuela", "Cortázar", 1963),
        ("Ficciones", "Borges", 1944),
        ("Bestiario", "Cortázar", 1951),
    ]:
        cliente.post("/libros", json={"titulo": titulo, "autor": autor, "anio": anio})


def test_obtener_o_crear_autor(app):
    with app.app_context():
        a = obtener_o_crear_autor("Borges")
        db.session.commit()
        b = obtener_o_crear_autor("Borges")
        assert a.id == b.id
        assert db.session.scalar(select(func.count()).select_from(Autor)) == 1


def test_crear_libro(cliente):
    r = cliente.post("/libros", json={"titulo": "Ficciones", "autor": "Borges", "anio": 1944})
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "titulo": "Ficciones", "autor": "Borges", "anio": 1944}


def test_crear_libro_invalido(cliente):
    r = cliente.post("/libros", json={"titulo": "Sin autor"})
    assert r.status_code == 400
    assert r.get_json() == {"error": "titulo y autor son obligatorios"}


def test_listar_ordenado_y_filtrado(cliente):
    cargar(cliente)
    titulos = [libro["titulo"] for libro in cliente.get("/libros").get_json()]
    assert titulos == ["Bestiario", "Ficciones", "Rayuela"]
    de_cortazar = cliente.get("/libros", query_string={"autor": "Cortázar"}).get_json()
    assert [libro["titulo"] for libro in de_cortazar] == ["Bestiario", "Rayuela"]
    assert all(libro["autor"] == "Cortázar" for libro in de_cortazar)


def test_autor_con_libros(cliente):
    cargar(cliente)
    r = cliente.get("/autores/1")
    assert r.status_code == 200
    assert r.get_json() == {"nombre": "Cortázar", "libros": ["Bestiario", "Rayuela"]}
    assert cliente.get("/autores/99").status_code == 404


def test_borrar(cliente):
    cargar(cliente)
    assert cliente.delete("/libros/2").status_code == 204
    assert [libro["titulo"] for libro in cliente.get("/libros").get_json()] == ["Bestiario", "Rayuela"]
    assert cliente.delete("/libros/2").status_code == 404
