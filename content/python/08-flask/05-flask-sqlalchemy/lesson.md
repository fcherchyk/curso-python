# Databases with Flask-SQLAlchemy

Flask doesn't ship a data layer: you pick one. The most common choice is **SQLAlchemy**, Python's
most widely used ORM, integrated through the **Flask-SQLAlchemy** extension, which handles the
per-request session, the configuration and a few shortcuts (`get_or_404`, pagination). What you
learn here about SQLAlchemy 2.0 also applies to FastAPI, which uses it without an extension.

## Configuration

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"    # or postgresql+psycopg://...
    app.config.update(config or {})
    db.init_app(app)
    with app.app_context():
        db.create_all()          # creates missing tables (in production: migrations)
    return app
```

`"sqlite://"` (no path) is an **in-memory** database: ideal for tests, because each app starts
empty.

## Models in the 2.0 (typed) style

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Author(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    year: Mapped[int | None]                              # nullable because it's Optional
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Author] = relationship(back_populates="books")
```

- `Mapped[T]` declares the column and its Python type. `T | None` makes it **nullable**.
- `mapped_column(...)` adds the details: primary key, length, `unique`, `index`, `default`.
- `relationship` defines the relationship **on the Python side**: `book.author` and
  `author.books`. `back_populates` keeps both sides in sync.
- Flask-SQLAlchemy derives the table name (`author`, `book`); with `__tablename__` you choose it
  yourself.

## The session: the "unit of work"

Every operation goes through `db.session`, which accumulates changes until `commit`:

```python
author = Author(name="Joyce")
db.session.add(author)
db.session.add(Book(title="Dubliners", author=author))   # assigning the object fills in the FK
db.session.commit()                                        # INSERTs in one transaction

author.name = "James Joyce"            # modifying is just assigning…
db.session.commit()                    # …and committing

db.session.delete(book)
db.session.commit()
```

If something fails midway, `db.session.rollback()` undoes what's pending. Flask-SQLAlchemy closes
the session automatically at the end of each request.

## Queries with `select()`

SQLAlchemy 2.0 uses a unified style: you build a `select` and execute it with the session.

```python
from sqlalchemy import select

book = db.session.get(Book, 3)                          # by primary key (or None)
book = db.get_or_404(Book, 3)                           # or abort with 404

stmt = select(Book).where(Book.year > 1950).order_by(Book.title)
books = db.session.scalars(stmt).all()                  # list of Book

joyce = db.session.scalars(
    select(Author).where(Author.name == "Joyce")
).first()                                               # the first one or None

# JOIN: an author's books by name
stmt = select(Book).join(Book.author).where(Author.name == "Joyce")

# Counting
from sqlalchemy import func
total = db.session.scalar(select(func.count()).select_from(Book))
```

- `.scalars(...)` returns model objects; `.all()`, `.first()` and `.one()` materialize them.
- `where` combines conditions with `and_`/`or_`, or with several arguments.
- The old API (`Book.query.filter_by(...)`) still exists, but it's considered *legacy*.

## The N+1 problem

```python
for book in db.session.scalars(select(Book)):
    print(book.author.name)          # one extra query PER book!
```

Relationships are loaded **lazily** by default: each `book.author` fires a SELECT. With 100
books, that's 101 queries. The fix is to ask for eager loading:

```python
from sqlalchemy.orm import selectinload, joinedload

stmt = select(Book).options(joinedload(Book.author))        # one JOIN
stmt = select(Author).options(selectinload(Author.books))   # one extra SELECT ... IN
```

## A typical CRUD

```python
@app.post("/books")
def create():
    data = request.get_json()
    book = Book(title=data["title"], author=get_or_create_author(data["author"]))
    db.session.add(book)
    db.session.commit()
    return {"id": book.id, "title": book.title}, 201         # the id exists after the commit
```

## Migrations

`db.create_all()` only **creates** tables that don't exist: it doesn't modify them. In a real
project, schema changes are versioned with **Alembic** (or **Flask-Migrate**, which integrates
it): `flask db migrate -m "add year"` and `flask db upgrade`.

## In the other frameworks

- **FastAPI**: the same SQLAlchemy 2.0, with the session as a dependency (`Depends(get_session)`).
- **Django**: its own ORM (`Book.objects.filter(year__gt=1950)`), with built-in migrations
  (`makemigrations`/`migrate`).

## Summary

- `db = SQLAlchemy(model_class=Base)` and `db.init_app(app)` in the factory.
- Typed models: `Mapped[T]`, `mapped_column` and `relationship(back_populates=...)`.
- `db.session.add/delete/commit`; `db.session.get` or `db.get_or_404` by primary key.
- Queries with `select(...).where(...).order_by(...)` and `db.session.scalars(...)`.
- Watch out for N+1: `joinedload`/`selectinload`.
- `create_all` to get started; Alembic migrations for real work.

## Exercise

The `Author` and `Book` models are already defined. Write the views for a library API: creation
with "get or create" for the author, a filtered and sorted listing, an author detail with their
books, and deletion.

**Further reading:** [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/),
[SQLAlchemy 2.0 ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).
