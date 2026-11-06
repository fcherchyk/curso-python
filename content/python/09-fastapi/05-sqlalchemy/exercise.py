"""Base de datos con SQLAlchemy 2.0.

Ya están el engine, el modelo Tarea y get_session. Escribí:

Schemas (Pydantic):
- TareaCrear: titulo (1 a 100 caracteres)
- TareaActualizar: titulo y hecha, ambos opcionales (PATCH)
- TareaPublica: id, titulo, hecha (con from_attributes=True)

Endpoints (todos usan la sesión de get_session):
- POST   /tareas           → 201 TareaPublica
- GET    /tareas           → lista ordenada por id; con ?hecha=true|false, filtrada
- GET    /tareas/{id}      → TareaPublica o 404 "tarea inexistente"
- PATCH  /tareas/{id}      → actualiza SOLO lo enviado (exclude_unset) o 404
- DELETE /tareas/{id}      → 204 o 404
"""

from collections.abc import Iterator
from typing import Annotated  # noqa: F401

from fastapi import Depends, FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel, ConfigDict, Field  # noqa: F401
from sqlalchemy import String, create_engine, select  # noqa: F401
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Tarea(Base):
    __tablename__ = "tareas"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    hecha: Mapped[bool] = mapped_column(default=False)


Base.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


app = FastAPI()
