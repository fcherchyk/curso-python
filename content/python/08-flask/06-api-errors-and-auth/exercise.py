"""REST APIs: errors, authentication and testing.

1. http_error: HTTPException handler → JSON {"error": e.name, "detail": e.description}, e.code
2. InvalidNote (domain exception): handler → 400 {"error": "Bad Request", "detail": str(e)}
3. require_token: decorator that reads "Authorization: Bearer <token>"
     - no header, or a different scheme → abort(401, description="missing token")
     - a token not in app.config["TOKENS"] → abort(401, description="invalid token")
     - if valid, stores the user in g.user
4. Routes:
     GET  /api/notes        (public)    → list of {"id", "author", "text"}
     GET  /api/me           (protected) → {"user": g.user}
     POST /api/notes        (protected) → body {"text"}; empty or missing text → raise InvalidNote("empty text")
                                          201 {"id", "author": g.user, "text"}
"""

import functools  # noqa: F401

from flask import Flask, abort, current_app, g, request  # noqa: F401
from werkzeug.exceptions import HTTPException  # noqa: F401


class InvalidNote(Exception):
    pass


def require_token(view):  # type: ignore[no-untyped-def]
    raise NotImplementedError("TODO")


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config["TOKENS"] = {}
    app.config.update(config or {})
    notes: list[dict[str, object]] = []  # noqa: F841  (this app's "database")

    # TODO: error handlers and routes

    return app
