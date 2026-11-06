"""Base de datos con Flask-SQLAlchemy.

Los modelos y create_app ya están. Escribí:

- obtener_o_crear_autor(nombre) → el Autor con ese nombre (lo crea si no existe, sin commit).
- POST   /libros               JSON {"titulo", "autor", "anio"?} → 201 {"id", "titulo", "autor", "anio"}
                               sin titulo o autor → 400 {"error": "titulo y autor son obligatorios"}
- GET    /libros               → lista de libros [{"id", "titulo", "autor", "anio"}] ordenada por título;
                               con ?autor=Nombre, solo los de ese autor
- GET    /autores/<int:id>     → {"nombre", "libros": [títulos ordenados]} o 404 (db.get_or_404)
- DELETE /libros/<int:id>      → 204 o 404

Registrá las rutas en el blueprint `bp` (ya se registra en create_app).
"""

from flask import Blueprint, Flask, request  # noqa: F401
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, select  # noqa: F401
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Autor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    libros: Mapped[list["Libro"]] = relationship(back_populates="autor")


class Libro(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    anio: Mapped[int | None]
    autor_id: Mapped[int] = mapped_column(ForeignKey("autor.id"))
    autor: Mapped[Autor] = relationship(back_populates="libros")


bp = Blueprint("biblioteca", __name__)


def obtener_o_crear_autor(nombre: str) -> Autor:
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
