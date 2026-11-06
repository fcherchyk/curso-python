from flask import Blueprint, Flask, current_app, redirect, url_for

api = Blueprint("api", __name__)
web = Blueprint("web", __name__)


@api.get("/estado")
def estado():
    return {"estado": "ok", "entorno": current_app.config["ENTORNO"]}


@api.get("/visitas")
def visitas():
    return {"visitas": current_app.extensions["contador"]["visitas"]}


@web.get("/")
def inicio():
    return f"{current_app.config['SALUDO']}, visitante"


@web.get("/ir-al-estado")
def ir_al_estado():
    return redirect(url_for("api.estado"))


class Contador:
    def init_app(self, app: Flask) -> None:
        # El estado vive en la app, no en la extensión: puede haber varias apps.
        app.extensions["contador"] = {"visitas": 0}

        @app.before_request
        def contar() -> None:
            app.extensions["contador"]["visitas"] += 1


contador = Contador()


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev", ENTORNO="desarrollo", SALUDO="Hola")
    if config:
        app.config.update(config)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(web)
    contador.init_app(app)
    return app
