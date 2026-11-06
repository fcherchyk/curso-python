from flask import Blueprint, Flask, current_app, redirect, url_for

api = Blueprint("api", __name__)
web = Blueprint("web", __name__)


@api.get("/status")
def status():
    return {"status": "ok", "environment": current_app.config["ENVIRONMENT"]}


@api.get("/visits")
def visits():
    return {"visits": current_app.extensions["counter"]["visits"]}


@web.get("/")
def index():
    return f"{current_app.config['GREETING']}, visitor"


@web.get("/go-to-status")
def go_to_status():
    return redirect(url_for("api.status"))


class Counter:
    def init_app(self, app: Flask) -> None:
        # The state lives in the app, not in the extension: there may be several apps.
        app.extensions["counter"] = {"visits": 0}

        @app.before_request
        def count() -> None:
            app.extensions["counter"]["visits"] += 1


counter = Counter()


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev", ENVIRONMENT="development", GREETING="Hello")
    if config:
        app.config.update(config)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(web)
    counter.init_app(app)
    return app
