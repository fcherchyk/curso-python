"""Databases with SQLAlchemy 2.0.

The engine, the Task model and get_session are already there. Write:

Schemas (Pydantic):
- TaskCreate: title (1 to 100 characters)
- TaskUpdate: title and done, both optional (PATCH)
- TaskPublic: id, title, done (with from_attributes=True)

Endpoints (all use the session from get_session):
- POST   /tasks            → 201 TaskPublic
- GET    /tasks            → list ordered by id; with ?done=true|false, filtered
- GET    /tasks/{id}       → TaskPublic or 404 "task not found"
- PATCH  /tasks/{id}       → updates ONLY what was sent (exclude_unset) or 404
- DELETE /tasks/{id}       → 204 or 404
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


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)


Base.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


app = FastAPI()
