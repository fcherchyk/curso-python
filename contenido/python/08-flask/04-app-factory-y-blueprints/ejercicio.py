"""App factory y blueprints.

1. Blueprint `api` (nombre "api"), registrado con url_prefix="/api":
     GET /api/estado → {"estado": "ok", "entorno": <config ENTORNO>}
2. Blueprint `web` (nombre "web"), sin prefijo:
     GET /            → texto "<config SALUDO>, visitante"
     GET /ir-al-estado → redirect a url_for("api.estado")
3. Extensión `Contador` con init_app(app): guarda {"visitas": 0} en
   app.extensions["contador"] y suma 1 antes de cada request (before_request).
     GET /api/visitas → {"visitas": <cantidad, contando este request>}
4. create_app(config=None): config por defecto SECRET_KEY="dev", ENTORNO="desarrollo",
   SALUDO="Hola"; `config` pisa los defaults. Registra los dos blueprints y la extensión.
"""

from flask import Blueprint, Flask, current_app, redirect, url_for  # noqa: F401

api = Blueprint("api", __name__)
web = Blueprint("web", __name__)


class Contador:
    def init_app(self, app: Flask) -> None:
        raise NotImplementedError("TODO")


contador = Contador()


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    # TODO: configuración, blueprints y extensión
    return app
