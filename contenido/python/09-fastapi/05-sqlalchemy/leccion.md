# Base de datos con SQLAlchemy 2.0

FastAPI no trae una capa de datos: la combinás. La opción estándar es **SQLAlchemy 2.0**, el mismo
ORM que usaste con Flask, pero acá **sin extensión**: la sesión se maneja con una **dependencia
con `yield`**. Además aparece una separación clave en las APIs tipadas: los **modelos del ORM**
(las tablas) son distintos de los **schemas de Pydantic** (lo que entra y sale por HTTP).

## Engine, sesión y modelos

```python
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

engine = create_engine("sqlite:///tareas.db")      # o postgresql+psycopg://user:pass@host/db
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Tarea(Base):
    __tablename__ = "tareas"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    hecha: Mapped[bool] = mapped_column(default=False)

Base.metadata.create_all(engine)                    # en serio: migraciones con Alembic
```

- El **engine** administra las conexiones (el pool).
- `sessionmaker` es una fábrica de sesiones configurada.
- Los modelos usan el mismo estilo tipado (`Mapped`, `mapped_column`) que en Flask-SQLAlchemy.

## La sesión como dependencia

```python
from collections.abc import Iterator
from typing import Annotated
from fastapi import Depends

def get_session() -> Iterator[Session]:
    with SessionLocal() as session:      # se cierra sola al terminar el request
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```

Cada request recibe **su propia sesión** y se cierra al final, pase lo que pase. En los tests, se
reemplaza con `dependency_overrides` por una sesión contra una base **en memoria y nueva**.

> SQLite en memoria + varios threads: usá
> `create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)`,
> así todas las conexiones comparten la misma base en memoria.

## Modelos del ORM vs. schemas de Pydantic

```python
from pydantic import BaseModel, ConfigDict, Field

class TareaCrear(BaseModel):                    # lo que el cliente ENVÍA para crear
    titulo: str = Field(min_length=1, max_length=100)

class TareaActualizar(BaseModel):               # PATCH: todo opcional
    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    hecha: bool | None = None

class TareaPublica(BaseModel):                  # lo que la API DEVUELVE
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str
    hecha: bool
```

¿Por qué no usar directamente el modelo del ORM en la API?

- El cliente **no debe** mandar ciertos campos (`id`, `creado_por`, `password_hash`).
- La respuesta **no debe** exponer otros (contraseñas, campos internos).
- La forma de la API y la de la tabla evolucionan por separado.

`from_attributes=True` permite construir el schema **desde un objeto del ORM**
(`TareaPublica.model_validate(tarea)`), y es lo que hace `response_model` cuando devolvés un
`Tarea`.

> **SQLModel** (del autor de FastAPI) fusiona las dos cosas en una sola clase, a cambio de menos
> separación. Es una alternativa válida para proyectos chicos.

## Un CRUD completo

```python
from sqlalchemy import select

@app.post("/tareas", response_model=TareaPublica, status_code=201)
def crear(datos: TareaCrear, session: SessionDep):
    tarea = Tarea(**datos.model_dump())
    session.add(tarea)
    session.commit()
    session.refresh(tarea)          # recarga el id y los defaults generados por la base
    return tarea                    # response_model lo convierte a TareaPublica

@app.get("/tareas", response_model=list[TareaPublica])
def listar(session: SessionDep, hecha: bool | None = None):
    stmt = select(Tarea).order_by(Tarea.id)
    if hecha is not None:
        stmt = stmt.where(Tarea.hecha == hecha)
    return session.scalars(stmt).all()

@app.get("/tareas/{id}", response_model=TareaPublica)
def detalle(id: int, session: SessionDep):
    tarea = session.get(Tarea, id)
    if tarea is None:
        raise HTTPException(404, "tarea inexistente")
    return tarea

@app.patch("/tareas/{id}", response_model=TareaPublica)
def actualizar(id: int, datos: TareaActualizar, session: SessionDep):
    tarea = session.get(Tarea, id)
    if tarea is None:
        raise HTTPException(404, "tarea inexistente")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)
    session.commit()
    session.refresh(tarea)
    return tarea
```

### PATCH y `exclude_unset`

En un PATCH, el cliente manda **solo lo que quiere cambiar**. `model_dump(exclude_unset=True)`
devuelve únicamente los campos que vinieron en el JSON. Sin eso, un PATCH con `{"hecha": true}`
pisaría el título con `None`.

## Endpoints `def` y la sesión sincrónica

SQLAlchemy con un driver sincrónico **bloquea**, así que estos endpoints son `def` y FastAPI los
corre en el thread pool (capítulo anterior). Si querés todo async, existe
`sqlalchemy.ext.asyncio` (`AsyncSession`, `create_async_engine`) con drivers como `asyncpg` o
`aiosqlite`: el código es casi igual, con `await`.

## En los otros frameworks

- **Flask**: el mismo SQLAlchemy, con Flask-SQLAlchemy manejando la sesión por request.
- **Django**: su propio ORM, y los **serializers** de DRF cumplen el rol de los schemas de Pydantic.

## Resumen

- Engine y `sessionmaker`; modelos tipados con `Mapped`.
- Sesión por request con una dependencia con `yield` (`SessionDep`).
- Schemas separados: `Crear`, `Actualizar` (opcional) y `Publica` (`from_attributes=True`).
- `session.add/commit/refresh`, `session.get` y `session.scalars(select(...))`.
- PATCH con `model_dump(exclude_unset=True)`.
- Endpoints `def` con la sesión sincrónica, o todo async con `AsyncSession`.

## Ejercicio

El engine, el modelo `Tarea` y `get_session` ya están. Escribí los schemas y el CRUD completo:
crear, listar con filtro, detalle, PATCH parcial y DELETE.

**Para profundizar:** [FastAPI: SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/),
[SQLAlchemy 2.0 Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/).
