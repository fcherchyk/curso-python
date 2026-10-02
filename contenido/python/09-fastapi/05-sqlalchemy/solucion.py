from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, create_engine, select
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


class TareaCrear(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)


class TareaActualizar(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    hecha: bool | None = None


class TareaPublica(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str
    hecha: bool


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


def buscar(session: Session, id: int) -> Tarea:
    tarea = session.get(Tarea, id)
    if tarea is None:
        raise HTTPException(404, "tarea inexistente")
    return tarea


@app.post("/tareas", response_model=TareaPublica, status_code=201)
def crear(datos: TareaCrear, session: SessionDep) -> Tarea:
    tarea = Tarea(**datos.model_dump())
    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea


@app.get("/tareas", response_model=list[TareaPublica])
def listar(session: SessionDep, hecha: bool | None = None) -> list[Tarea]:
    stmt = select(Tarea).order_by(Tarea.id)
    if hecha is not None:
        stmt = stmt.where(Tarea.hecha == hecha)
    return list(session.scalars(stmt))


@app.get("/tareas/{id}", response_model=TareaPublica)
def detalle(id: int, session: SessionDep) -> Tarea:
    return buscar(session, id)


@app.patch("/tareas/{id}", response_model=TareaPublica)
def actualizar(id: int, datos: TareaActualizar, session: SessionDep) -> Tarea:
    tarea = buscar(session, id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(tarea, campo, valor)
    session.commit()
    session.refresh(tarea)
    return tarea


@app.delete("/tareas/{id}", status_code=204)
def borrar(id: int, session: SessionDep) -> None:
    session.delete(buscar(session, id))
    session.commit()
