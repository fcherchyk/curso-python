import functools

from flask import Flask, abort, current_app, g, request
from werkzeug.exceptions import HTTPException


class NotaInvalida(Exception):
    pass


def requiere_token(vista):  # type: ignore[no-untyped-def]
    @functools.wraps(vista)
    def envoltura(*args, **kwargs):  # type: ignore[no-untyped-def]
        esquema, _, token = request.headers.get("Authorization", "").partition(" ")
        if esquema != "Bearer" or not token:
            abort(401, description="falta el token")
        usuario = current_app.config["TOKENS"].get(token)
        if usuario is None:
            abort(401, description="token inválido")
        g.usuario = usuario
        return vista(*args, **kwargs)

    return envoltura


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config["TOKENS"] = {}
    app.config.update(config or {})
    notas: list[dict[str, object]] = []

    @app.errorhandler(HTTPException)
    def error_http(e: HTTPException):  # type: ignore[no-untyped-def]
        return {"error": e.name, "detalle": e.description}, e.code

    @app.errorhandler(NotaInvalida)
    def nota_invalida(e: NotaInvalida):  # type: ignore[no-untyped-def]
        return {"error": "Bad Request", "detalle": str(e)}, 400

    @app.get("/api/notas")
    def listar_notas():  # type: ignore[no-untyped-def]
        return notas

    @app.get("/api/yo")
    @requiere_token
    def yo():  # type: ignore[no-untyped-def]
        return {"usuario": g.usuario}

    @app.post("/api/notas")
    @requiere_token
    def crear_nota():  # type: ignore[no-untyped-def]
        texto = (request.get_json(silent=True) or {}).get("texto", "")
        if not texto:
            raise NotaInvalida("texto vacío")
        nota = {"id": len(notas) + 1, "autor": g.usuario, "texto": texto}
        notas.append(nota)
        return nota, 201

    return app
