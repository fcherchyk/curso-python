"""Dependency injection with Depends.

Dependencies to write:
- pagination(page=1 (≥1), per_page=10 (≥1, ≤50)) → Page(offset, limit)
- current_user(authorization: header) → User
    no header or no "Bearer " → 401 detail "missing token" (header WWW-Authenticate: Bearer)
    token not in TOKENS → 401 detail "invalid token"
- admin_only(user = Depends(current_user)) → the user, or 403 detail "admin required"
- get_repo() → ProductRepo (already written: returns REPO)

Endpoints:
- GET    /products              → repo.list_page(offset, limit)  (paginated)
- GET    /me                    → {"name", "is_admin"} of the current user
- DELETE /products/{id}         → admin only; repo.delete(id) → 204, or 404 if it didn't exist
"""

from dataclasses import dataclass, field
from typing import Annotated  # noqa: F401

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status  # noqa: F401


@dataclass
class User:
    name: str
    is_admin: bool = False


TOKENS = {"t-alice": User("alice", is_admin=True), "t-bob": User("bob")}


@dataclass
class Page:
    offset: int
    limit: int


@dataclass
class ProductRepo:
    products: list[str] = field(default_factory=list)

    def list_page(self, offset: int, limit: int) -> list[str]:
        return self.products[offset : offset + limit]

    def delete(self, index: int) -> bool:
        if 0 <= index < len(self.products):
            del self.products[index]
            return True
        return False


REPO = ProductRepo([f"product {i}" for i in range(1, 26)])


def get_repo() -> ProductRepo:
    return REPO


def pagination() -> Page:  # ← add the parameters
    raise NotImplementedError("TODO")


def current_user() -> User:  # ← add the header
    raise NotImplementedError("TODO")


def admin_only() -> User:  # ← make it depend on current_user
    raise NotImplementedError("TODO")


app = FastAPI()
