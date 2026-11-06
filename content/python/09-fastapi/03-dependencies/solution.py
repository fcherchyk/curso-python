from dataclasses import asdict, dataclass, field
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status


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


def pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=50)] = 10,
) -> Page:
    return Page(offset=(page - 1) * per_page, limit=per_page)


def current_user(authorization: Annotated[str | None, Header()] = None) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = TOKENS.get(authorization.removeprefix("Bearer "))
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return user


def admin_only(user: Annotated[User, Depends(current_user)]) -> User:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="admin required")
    return user


Repo = Annotated[ProductRepo, Depends(get_repo)]

app = FastAPI()


@app.get("/products")
def list_products(page: Annotated[Page, Depends(pagination)], repo: Repo) -> list[str]:
    return repo.list_page(page.offset, page.limit)


@app.get("/me")
def me(user: Annotated[User, Depends(current_user)]) -> dict[str, object]:
    return asdict(user)


@app.delete("/products/{id}", status_code=204, dependencies=[Depends(admin_only)])
def delete_product(id: int, repo: Repo) -> None:
    if not repo.delete(id):
        raise HTTPException(404, "product not found")
