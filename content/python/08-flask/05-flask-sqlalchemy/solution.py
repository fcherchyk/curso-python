from flask import Blueprint, Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, select
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


def a_dict(libro: Libro) -> dict[str, object]:
    return {"id": libro.id, "titulo": libro.titulo, "autor": libro.autor.nombre, "anio": libro.anio}


def obtener_o_crear_autor(nombre: str) -> Autor:
    autor = db.session.scalars(select(Autor).where(Autor.nombre == nombre)).first()
    if autor is None:
        autor = Autor(nombre=nombre)
        db.session.add(autor)
    return autor


@bp.post("/libros")
def crear_libro():
    datos = request.get_json(silent=True) or {}
    if not datos.get("titulo") or not datos.get("autor"):
        return {"error": "titulo y autor son obligatorios"}, 400
    libro = Libro(
        titulo=datos["titulo"],
        anio=datos.get("anio"),
        autor=obtener_o_crear_autor(datos["autor"]),
    )
    db.session.add(libro)
    db.session.commit()
    return a_dict(libro), 201


@bp.get("/libros")
def listar_libros():
    stmt = select(Libro).join(Libro.autor).order_by(Libro.titulo)
    if autor := request.args.get("autor"):
        stmt = stmt.where(Autor.nombre == autor)
    return [a_dict(libro) for libro in db.session.scalars(stmt)]


@bp.get("/autores/<int:id>")
def detalle_autor(id: int):
    autor = db.get_or_404(Autor, id)
    return {"nombre": autor.nombre, "libros": sorted(libro.titulo for libro in autor.libros)}


@bp.delete("/libros/<int:id>")
def borrar_libro(id: int):
    libro = db.get_or_404(Libro, id)
    db.session.delete(libro)
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
