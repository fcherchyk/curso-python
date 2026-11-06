# Dependency injection with `Depends`

FastAPI's most powerful feature is its **dependency** system. A dependency is a function that
FastAPI runs **before** your endpoint to give it something it needs: the authenticated user, a
database session, the configuration or the pagination parameters. With a single idea it solves
what in Flask took decorators, `g` and `current_app`, and it makes everything **easy to swap
out in tests**.

## The basics

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Query

def pagination(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, int]:
    return {"offset": (page - 1) * per_page, "limit": per_page}

@app.get("/products")
def list_products(pag: Annotated[dict[str, int], Depends(pagination)]):
    return PRODUCTS[pag["offset"] : pag["offset"] + pag["limit"]]
```

- `Depends(function)` tells FastAPI: "before calling the endpoint, call `function` and pass me
  what it returns".
- The dependency **declares its own parameters** (query, headers, other dependencies) and
  FastAPI resolves them just like an endpoint's. They show up in `/docs`.
- `Annotated[T, Depends(f)]` is the recommended form. You can also define an alias,
  `Pagination = Annotated[dict, Depends(pagination)]`, and use it in many endpoints.

## Authentication as a dependency

```python
from fastapi import Header, HTTPException, status

def current_user(authorization: Annotated[str | None, Header()] = None) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = find_by_token(authorization.removeprefix("Bearer "))
    if user is None:
        raise HTTPException(401, detail="invalid token")
    return user

@app.get("/me")
def me(user: Annotated[User, Depends(current_user)]):
    return user
```

- `Header()` reads a header. The parameter name is converted: `authorization` →
  `Authorization`, `x_token` → `X-Token`.
- If the dependency **raises** `HTTPException`, the endpoint never runs.
- FastAPI ships utilities like `OAuth2PasswordBearer` and `HTTPBearer`, which also wire up the
  "Authorize" button in `/docs`.

## Sub-dependencies: composing

Dependencies can depend on others, forming a chain:

```python
def admin_only(user: Annotated[User, Depends(current_user)]) -> User:
    if not user.is_admin:
        raise HTTPException(403, "administrator permissions required")
    return user

@app.delete("/products/{id}", status_code=204)
def delete_product(id: int, admin: Annotated[User, Depends(admin_only)]): ...
```

FastAPI builds the graph and **caches each dependency within the same request**: if two
dependencies ask for `current_user`, it runs only once.

If you don't need the value, the dependency can go in the decorator:
`@app.delete(..., dependencies=[Depends(admin_only)])`. Or on an entire router.

## Dependencies with `yield`: setup and cleanup

```python
def get_session():
    session = SessionLocal()
    try:
        yield session            # the endpoint uses the session
    finally:
        session.close()          # runs after the response is sent
```

It's the same pattern as the context managers from module 04. This is how the database
session is handled in the SQLAlchemy chapter.

## Injecting services and configuration

```python
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:          # created only once
    return Settings()

def get_repo() -> ProductRepository:
    return SQLRepository(...)

@app.get("/products")
def list_products(repo: Annotated[ProductRepository, Depends(get_repo)]):
    return repo.list_all()
```

The endpoint doesn't know **where** the repository comes from: it just declares that it needs
one. That's the dependency inversion from the testing module, now built into the framework.

## Tests: `dependency_overrides`

The big win: in tests you replace any dependency without patching anything.

```python
def fake_repo():
    return InMemoryRepository([...])

def test_list():
    app.dependency_overrides[get_repo] = fake_repo
    app.dependency_overrides[current_user] = lambda: User(name="test", is_admin=True)
    try:
        r = TestClient(app).get("/products")
        ...
    finally:
        app.dependency_overrides.clear()
```

The dict key is the **original function** and the value is its replacement.

## Comparison

| Need                   | Flask                          | FastAPI                                  |
|------------------------|--------------------------------|------------------------------------------|
| authenticated user     | decorator + `g.user`           | `Depends(current_user)`                  |
| configuration          | `current_app.config`           | `Depends(get_settings)`                  |
| database session       | `db.session` (scoped)          | `Depends(get_session)` with `yield`      |
| swapping in tests      | factory config or mocks        | `app.dependency_overrides`               |
| composed permissions   | stacked decorators             | sub-dependencies                         |

## Summary

- `Depends(f)`: FastAPI calls `f` (resolving its parameters) and passes the result to the endpoint.
- Authentication, pagination, configuration and repositories as dependencies.
- Sub-dependencies compose and are cached within each request.
- `yield` for setup and cleanup (sessions).
- `app.dependency_overrides[original] = fake` for testing.

## Exercise

Pagination, token authentication, a composed admin permission and an injected repository that
the tests replace with `dependency_overrides`.

**Further reading:** [FastAPI: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/),
[Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
