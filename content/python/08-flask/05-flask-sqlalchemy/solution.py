from flask import Blueprint, Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, select
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


def to_dict(book: Book) -> dict[str, object]:
    return {"id": book.id, "title": book.title, "author": book.author.name, "year": book.year}


def get_or_create_author(name: str) -> Author:
    author = db.session.scalars(select(Author).where(Author.name == name)).first()
    if author is None:
        author = Author(name=name)
        db.session.add(author)
    return author


@bp.post("/books")
def create_book():
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("author"):
        return {"error": "title and author are required"}, 400
    book = Book(
        title=data["title"],
        year=data.get("year"),
        author=get_or_create_author(data["author"]),
    )
    db.session.add(book)
    db.session.commit()
    return to_dict(book), 201


@bp.get("/books")
def list_books():
    stmt = select(Book).join(Book.author).order_by(Book.title)
    if author := request.args.get("author"):
        stmt = stmt.where(Author.name == author)
    return [to_dict(book) for book in db.session.scalars(stmt)]


@bp.get("/authors/<int:id>")
def author_detail(id: int):
    author = db.get_or_404(Author, id)
    return {"name": author.name, "books": sorted(book.title for book in author.books)}


@bp.delete("/books/<int:id>")
def delete_book(id: int):
    book = db.get_or_404(Book, id)
    db.session.delete(book)
    db.session.commit()
    return "", 204


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config.update(config or {})
    db.init_app(app)
    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    return app
