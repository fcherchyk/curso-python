# Base de datos con Flask-SQLAlchemy

Flask no trae una capa de datos: la elegís vos. La opción más común es **SQLAlchemy**, el ORM
más usado de Python, integrado con la extensión **Flask-SQLAlchemy**, que se encarga de la
sesión por request, de la configuración y de algunos atajos (`get_or_404`, paginación). Lo que
aprendas acá sobre SQLAlchemy 2.0 te sirve también en FastAPI, que lo usa sin extensión.

## Configuración

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"   # o postgresql+psycopg://...
    app.config.update(config or {})
    db.init_app(app)
    with app.app_context():
        db.create_all()          # crea las tablas que falten (en producción: migraciones)
    return app
```

`"sqlite://"` (sin ruta) es una base **en memoria**: ideal para tests, porque cada app arranca
vacía.

## Modelos con el estilo 2.0 (tipado)

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Autor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    libros: Mapped[list["Libro"]] = relationship(back_populates="autor")

class Libro(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    anio: Mapped[int | None]                              # nullable porque es Optional
    autor_id: Mapped[int] = mapped_column(ForeignKey("autor.id"))
    autor: Mapped[Autor] = relationship(back_populates="libros")
```

- `Mapped[T]` declara la columna y su tipo de Python. `T | None` la hace **nullable**.
- `mapped_column(...)` agrega los detalles: clave primaria, longitud, `unique`, `index`, `default`.
- `relationship` define la relación **del lado de Python**: `libro.autor` y `autor.libros`.
  `back_populates` mantiene sincronizados los dos lados.
- Flask-SQLAlchemy deduce el nombre de la tabla (`autor`, `libro`); con `__tablename__` lo elegís
  vos.

## La sesión: la "unidad de trabajo"

Todas las operaciones pasan por `db.session`, que acumula los cambios hasta el `commit`:

```python
autor = Autor(nombre="Borges")
db.session.add(autor)
db.session.add(Libro(titulo="Ficciones", autor=autor))   # asignar el objeto completa la FK
db.session.commit()                                        # INSERTs en una transacción

autor.nombre = "Jorge Luis Borges"     # modificar es asignar…
db.session.commit()                    # …y commitear

db.session.delete(libro)
db.session.commit()
```

Si algo falla en el medio, `db.session.rollback()` deshace lo pendiente. Flask-SQLAlchemy
cierra la sesión automáticamente al terminar cada request.

## Consultas con `select()`

SQLAlchemy 2.0 usa un estilo unificado: se arma un `select` y se ejecuta con la sesión.

```python
from sqlalchemy import select

libro = db.session.get(Libro, 3)                        # por clave primaria (o None)
libro = db.get_or_404(Libro, 3)                         # o aborta con 404

stmt = select(Libro).where(Libro.anio > 1950).order_by(Libro.titulo)
libros = db.session.scalars(stmt).all()                 # lista de Libro

borges = db.session.scalars(
    select(Autor).where(Autor.nombre == "Borges")
).first()                                               # el primero o None

# JOIN: libros de un autor por nombre
stmt = select(Libro).join(Libro.autor).where(Autor.nombre == "Borges")

# Contar
from sqlalchemy import func
total = db.session.scalar(select(func.count()).select_from(Libro))
```

- `.scalars(...)` devuelve objetos del modelo; `.all()`, `.first()` y `.one()` los materializan.
- `where` combina condiciones con `and_`/`or_`, o con varios argumentos.
- La API vieja (`Libro.query.filter_by(...)`) sigue existiendo, pero está considerada *legacy*.

## El problema N+1

```python
for libro in db.session.scalars(select(Libro)):
    print(libro.autor.nombre)        # ¡una consulta extra POR libro!
```

Las relaciones se cargan de forma **perezosa** por defecto: cada `libro.autor` dispara un
SELECT. Con 100 libros, son 101 consultas. La solución es pedir la carga anticipada:

```python
from sqlalchemy.orm import selectinload, joinedload

stmt = select(Libro).options(joinedload(Libro.autor))       # un JOIN
stmt = select(Autor).options(selectinload(Autor.libros))    # un SELECT ... IN extra
```

## Un CRUD típico

```python
@app.post("/libros")
def crear():
    datos = request.get_json()
    libro = Libro(titulo=datos["titulo"], autor=obtener_o_crear_autor(datos["autor"]))
    db.session.add(libro)
    db.session.commit()
    return {"id": libro.id, "titulo": libro.titulo}, 201     # el id ya existe después del commit
```

## Migraciones

`db.create_all()` solo **crea** tablas que no existen: no las modifica. En un proyecto real, los
cambios de esquema se versionan con **Alembic** (o **Flask-Migrate**, que lo integra):
`flask db migrate -m "agrega año"` y `flask db upgrade`.

## En los otros frameworks

- **FastAPI**: el mismo SQLAlchemy 2.0, con la sesión como dependencia (`Depends(get_session)`).
- **Django**: su propio ORM (`Libro.objects.filter(anio__gt=1950)`), con migraciones incorporadas
  (`makemigrations`/`migrate`).

## Resumen

- `db = SQLAlchemy(model_class=Base)` y `db.init_app(app)` en la factory.
- Modelos tipados: `Mapped[T]`, `mapped_column` y `relationship(back_populates=...)`.
- `db.session.add/delete/commit`; `db.session.get` o `db.get_or_404` por clave primaria.
- Consultas con `select(...).where(...).order_by(...)` y `db.session.scalars(...)`.
- Cuidado con el N+1: `joinedload`/`selectinload`.
- `create_all` para empezar; migraciones con Alembic en serio.

## Ejercicio

Los modelos `Autor` y `Libro` ya están definidos. Escribí las vistas de una API de biblioteca:
alta con "obtener o crear" el autor, listado filtrado y ordenado, detalle de un autor con sus
libros y borrado.

**Para profundizar:** [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/),
[SQLAlchemy 2.0 ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).
