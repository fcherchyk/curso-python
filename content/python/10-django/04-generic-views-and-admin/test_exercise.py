import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="exercise",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "django.contrib.sessions",
        "django.contrib.messages",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
            "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
        }
    ],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
)
django.setup()

import re

import pytest
from django.contrib import admin
from django.db import connection
from django.test import Client
from exercise import Book

BOOKS = [
    ("Hopscotch", "Cortazar", 1963),
    ("Ficciones", "Borges", 1944),
    ("The Tunnel", "Sabato", 1948),
    ("Bestiary", "Cortazar", 1951),
    ("The Aleph", "Borges", 1949),
]


@pytest.fixture(autouse=True)
def data():
    with connection.schema_editor() as editor:
        editor.create_model(Book)
    for title, author, year in BOOKS:
        Book.objects.create(title=title, author=author, year=year)
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Book)


def titles(html: str) -> list[str]:
    return re.findall(r'<a href="/books/\d+/">([^<]+)</a>', html)


def test_list_ordered_and_paginated():
    c = Client()
    html = c.get("/books/").content.decode()
    assert titles(html) == ["Bestiary", "Ficciones", "Hopscotch"]
    assert "Page 1 of 2" in html
    assert titles(c.get("/books/", {"page": 2}).content.decode()) == ["The Aleph", "The Tunnel"]


def test_list_with_search():
    html = Client().get("/books/", {"q": "THE "}).content.decode()
    assert titles(html) == ["The Aleph", "The Tunnel"]
    html = Client().get("/books/", {"q": "zzz"}).content.decode()
    assert "No books" in html


def test_detail():
    book = Book.objects.get(title="Ficciones")
    html = Client().get(f"/books/{book.pk}/").content.decode()
    assert "<h1>Ficciones</h1>" in html and "Borges" in html
    assert Client().get("/books/999/").status_code == 404


def test_create_validates_and_redirects():
    c = Client()
    assert c.get("/books/new/").status_code == 200
    r = c.post("/books/new/", {"title": "Zama", "author": "Di Benedetto", "year": 1956})
    assert r.status_code == 302
    assert r.headers["Location"] == "/books/"
    assert Book.objects.filter(title="Zama").exists()
    r = c.post("/books/new/", {"title": "", "author": "X", "year": "no"})
    assert r.status_code == 200, "with errors it re-renders the form"
    assert Book.objects.count() == 6


def test_admin_registered():
    assert admin.site.is_registered(Book)
    model_admin = admin.site._registry[Book]
    assert list(model_admin.list_display) == ["title", "author", "year"]
    assert list(model_admin.search_fields) == ["title", "author"]
    assert list(model_admin.list_filter) == ["year"]
