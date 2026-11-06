# REST APIs: errors, authentication and testing

A serious API has to respond **in JSON every time**, even when something goes wrong. It also has
to protect its endpoints and be covered by reliable tests. In this chapter we build all three
pieces with Flask: global error handlers, a token authentication decorator plus the `g` context,
and well-organized pytest fixtures.

## Errors in JSON: `errorhandler`

By default, `abort(404)` returns an HTML page. For an API, you register a handler:

```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def http_error(e: HTTPException):
    return {"error": e.name, "detail": e.description}, e.code
```

Since every Werkzeug HTTP exception inherits from `HTTPException`, a single handler covers 400,
401, 403, 404, 405, etc., including unknown routes and disallowed methods.

You can also map **your domain exceptions** to HTTP codes:

```python
class NotFoundError(Exception): ...

@app.errorhandler(NotFoundError)
def not_found(e):
    return {"error": "Not Found", "detail": str(e)}, 404

@app.errorhandler(ValueError)
def invalid_value(e):
    return {"error": "Bad Request", "detail": str(e)}, 400
```

That way the business logic raises ordinary Python exceptions and the HTTP layer decides how to
respond. It's the same idea as FastAPI's `exception_handler`.

For 500 errors, `@app.errorhandler(Exception)` catches everything else: **log the traceback** and
return a generic message, with no internal details. With `TESTING=True`, Flask lets exceptions
reach the test so you see the real error.

## Token authentication with a decorator

The simplest pattern for an API is a **token** in the `Authorization: Bearer <token>` header:

```python
import functools
from flask import abort, current_app, g, request

def require_token(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        scheme, _, token = header.partition(" ")
        if scheme != "Bearer" or not token:
            abort(401, description="missing token")
        user = current_app.config["TOKENS"].get(token)
        if user is None:
            abort(401, description="invalid token")
        g.user = user                        # available for the rest of this request
        return view(*args, **kwargs)
    return wrapper

@app.get("/api/me")
@require_token
def me():
    return {"user": g.user}
```

- It's a **decorator** like the ones in module 04, and `functools.wraps` is essential: Flask uses
  the function name as the endpoint, and without `wraps` two protected views would clash.
- Order matters: `@app.get` goes **on top** (it's applied last), so the protected version is
  what gets registered.
- `g` is a **per-request** "global" object for data shared by the functions in that request, like
  the authenticated user or the database connection.
- **401** means "I don't know who you are" (the credential is missing or invalid); **403** means
  "I know who you are, but you can't do that".

In production, tokens are usually **JWTs** (signed, with expiration) or opaque tokens stored in
the database, and they're compared with `secrets.compare_digest` to prevent timing attacks. For
login-based sessions, use **Flask-Login**.

## pytest fixtures for Flask

```python
# conftest.py
import pytest
from store import create_app

@pytest.fixture
def app():
    return create_app({"TESTING": True, "TOKENS": {"t-alice": "alice"}})

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth():
    return {"Authorization": "Bearer t-alice"}
```

```python
def test_me(client, auth):
    assert client.get("/api/me", headers=auth).get_json() == {"user": "alice"}

def test_me_without_token(client):
    r = client.get("/api/me")
    assert r.status_code == 401
    assert r.get_json()["detail"] == "missing token"
```

Fixtures compose (`client` depends on `app`) and each test gets fresh instances. Test **the error
cases as carefully as the happy path**: they're the ones that break most often.

## REST design in two minutes

| Action               | Method and route         | Typical response         |
|----------------------|--------------------------|--------------------------|
| list                 | `GET /notes`             | 200 + list               |
| detail               | `GET /notes/7`           | 200 or 404               |
| create               | `POST /notes`            | 201 + created resource   |
| replace/update       | `PUT`/`PATCH /notes/7`   | 200 or 204               |
| delete               | `DELETE /notes/7`        | 204                      |

Routes are **plural nouns**; the method supplies the action. Errors always have the same shape
(for example `{"error", "detail"}`), so API consumers can handle them uniformly.

## In the other frameworks

- **FastAPI** handles authentication with **dependencies** (`Depends(current_user)`) instead of
  decorators, and validates the body automatically with Pydantic.
- **Django REST Framework** ships authentication and permission classes (`IsAuthenticated`) and a
  standard error format.

## Summary

- `@app.errorhandler(HTTPException)` so every HTTP error comes out as JSON.
- Map domain exceptions to HTTP codes with your own handlers.
- Authentication with a decorator that reads `Authorization: Bearer ...`, stores the user in `g`
  and uses `functools.wraps`.
- 401 = not authenticated; 403 = not allowed.
- `app` → `client` → `auth` fixtures in `conftest.py`; test the errors too.

## Exercise

A notes API with JSON errors, a token decorator and a domain exception mapped to 400.

**Further reading:** [Handling Application Errors](https://flask.palletsprojects.com/en/stable/errorhandling/),
[View Decorators](https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/).
