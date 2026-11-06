import functools

from flask import Flask, abort, current_app, g, request
from werkzeug.exceptions import HTTPException


class InvalidNote(Exception):
    pass


def require_token(view):  # type: ignore[no-untyped-def]
    @functools.wraps(view)
    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        scheme, _, token = request.headers.get("Authorization", "").partition(" ")
        if scheme != "Bearer" or not token:
            abort(401, description="missing token")
        user = current_app.config["TOKENS"].get(token)
        if user is None:
            abort(401, description="invalid token")
        g.user = user
        return view(*args, **kwargs)

    return wrapper


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config["TOKENS"] = {}
    app.config.update(config or {})
    notes: list[dict[str, object]] = []

    @app.errorhandler(HTTPException)
    def http_error(e: HTTPException):  # type: ignore[no-untyped-def]
        return {"error": e.name, "detail": e.description}, e.code

    @app.errorhandler(InvalidNote)
    def invalid_note(e: InvalidNote):  # type: ignore[no-untyped-def]
        return {"error": "Bad Request", "detail": str(e)}, 400

    @app.get("/api/notes")
    def list_notes():  # type: ignore[no-untyped-def]
        return notes

    @app.get("/api/me")
    @require_token
    def me():  # type: ignore[no-untyped-def]
        return {"user": g.user}

    @app.post("/api/notes")
    @require_token
    def create_note():  # type: ignore[no-untyped-def]
        text = (request.get_json(silent=True) or {}).get("text", "")
        if not text:
            raise InvalidNote("empty text")
        note = {"id": len(notes) + 1, "author": g.user, "text": text}
        notes.append(note)
        return note, 201

    return app
