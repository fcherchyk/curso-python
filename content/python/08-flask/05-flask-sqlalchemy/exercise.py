"""Databases with Flask-SQLAlchemy.

The models and create_app are already done. Write:

- get_or_create_author(name) → the Author with that name (creates it if missing, no commit).
- POST   /books                JSON {"title", "author", "year"?} → 201 {"id", "title", "author", "year"}
                               no title or author → 400 {"error": "title and author are required"}
- GET    /books                → list of books [{"id", "title", "author", "year"}] sorted by title;
                               with ?author=Name, only that author's books
- GET    /authors/<int:id>     → {"name", "books": [sorted titles]} or 404 (db.get_or_404)
- DELETE /books/<int:id>       → 204 or 404

Register the routes on the `bp` blueprint (create_app already registers it).
"""

from flask import Blueprint, Flask, request  # noqa: F401
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, select  # noqa: F401
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    year: Mapped[int | None]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(back_populates="books")


bp = Blueprint("library", __name__)


def get_or_create_author(name: str) -> Author:
    raise NotImplementedError("TODO")


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config.update(config or {})
    db.init_app(app)
    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    return app
