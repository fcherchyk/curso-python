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


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)


Base.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    done: bool | None = None


class TaskPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    done: bool


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


def find_task(session: Session, id: int) -> Task:
    task = session.get(Task, id)
    if task is None:
        raise HTTPException(404, "task not found")
    return task


@app.post("/tasks", response_model=TaskPublic, status_code=201)
def create(data: TaskCreate, session: SessionDep) -> Task:
    task = Task(**data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks", response_model=list[TaskPublic])
def list_tasks(session: SessionDep, done: bool | None = None) -> list[Task]:
    stmt = select(Task).order_by(Task.id)
    if done is not None:
        stmt = stmt.where(Task.done == done)
    return list(session.scalars(stmt))


@app.get("/tasks/{id}", response_model=TaskPublic)
def detail(id: int, session: SessionDep) -> Task:
    return find_task(session, id)


@app.patch("/tasks/{id}", response_model=TaskPublic)
def update(id: int, data: TaskUpdate, session: SessionDep) -> Task:
    task = find_task(session, id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{id}", status_code=204)
def delete(id: int, session: SessionDep) -> None:
    session.delete(find_task(session, id))
    session.commit()
