"""APIs REST: errores, autenticación y testing.

1. error_http: handler de HTTPException → JSON {"error": e.name, "detalle": e.description}, e.code
2. NotaInvalida (excepción de dominio): handler → 400 {"error": "Bad Request", "detalle": str(e)}
3. requiere_token: decorador que lee "Authorization: Bearer <token>"
     - sin header o con otro esquema → abort(401, description="falta el token")
     - token que no está en app.config["TOKENS"] → abort(401, description="token inválido")
     - si es válido, guarda el usuario en g.usuario
4. Rutas:
     GET  /api/notas        (pública)   → lista de {"id", "autor", "texto"}
     GET  /api/yo           (protegida) → {"usuario": g.usuario}
     POST /api/notas        (protegida) → body {"texto"}; texto vacío o ausente → raise NotaInvalida("texto vacío")
                                          201 {"id", "autor": g.usuario, "texto"}
"""

import functools  # noqa: F401

from flask import Flask, abort, current_app, g, request  # noqa: F401
from werkzeug.exceptions import HTTPException  # noqa: F401


class NotaInvalida(Exception):
    pass


def requiere_token(vista):  # type: ignore[no-untyped-def]
    raise NotImplementedError("TODO")


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config["TOKENS"] = {}
    app.config.update(config or {})
    notas: list[dict[str, object]] = []  # noqa: F841  ("base de datos" de esta app)

    # TODO: error handlers y rutas

    return app
