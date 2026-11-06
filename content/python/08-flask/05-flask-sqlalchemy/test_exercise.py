import pytest
from exercise import Author, create_app, db, get_or_create_author
from sqlalchemy import func, select


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def load(client):
    for title, author, year in [
        ("Persuasion", "Austen", 1817),
        ("Dubliners", "Joyce", 1914),
        ("Emma", "Austen", 1815),
    ]:
        client.post("/books", json={"title": title, "author": author, "year": year})


def test_get_or_create_author(app):
    with app.app_context():
        a = get_or_create_author("Joyce")
        db.session.commit()
        b = get_or_create_author("Joyce")
        assert a.id == b.id
        assert db.session.scalar(select(func.count()).select_from(Author)) == 1


def test_create_book(client):
    r = client.post("/books", json={"title": "Dubliners", "author": "Joyce", "year": 1914})
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "title": "Dubliners", "author": "Joyce", "year": 1914}


def test_create_book_invalid(client):
    r = client.post("/books", json={"title": "No author"})
    assert r.status_code == 400
    assert r.get_json() == {"error": "title and author are required"}


def test_list_sorted_and_filtered(client):
    load(client)
    titles = [book["title"] for book in client.get("/books").get_json()]
    assert titles == ["Dubliners", "Emma", "Persuasion"]
    by_austen = client.get("/books", query_string={"author": "Austen"}).get_json()
    assert [book["title"] for book in by_austen] == ["Emma", "Persuasion"]
    assert all(book["author"] == "Austen" for book in by_austen)


def test_author_with_books(client):
    load(client)
    r = client.get("/authors/1")
    assert r.status_code == 200
    assert r.get_json() == {"name": "Austen", "books": ["Emma", "Persuasion"]}
    assert client.get("/authors/99").status_code == 404


def test_delete(client):
    load(client)
    assert client.delete("/books/2").status_code == 204
    assert [book["title"] for book in client.get("/books").get_json()] == ["Emma", "Persuasion"]
    assert client.delete("/books/2").status_code == 404
