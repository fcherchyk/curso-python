"""App factory and blueprints.

1. Blueprint `api` (name "api"), registered with url_prefix="/api":
     GET /api/status → {"status": "ok", "environment": <config ENVIRONMENT>}
2. Blueprint `web` (name "web"), no prefix:
     GET /             → text "<config GREETING>, visitor"
     GET /go-to-status → redirect to url_for("api.status")
3. `Counter` extension with init_app(app): stores {"visits": 0} in
   app.extensions["counter"] and adds 1 before each request (before_request).
     GET /api/visits → {"visits": <count, including this request>}
4. create_app(config=None): default config SECRET_KEY="dev", ENVIRONMENT="development",
   GREETING="Hello"; `config` overrides the defaults. Registers both blueprints and the extension.
"""

from flask import Blueprint, Flask, current_app, redirect, url_for  # noqa: F401

api = Blueprint("api", __name__)
web = Blueprint("web", __name__)


class Counter:
    def init_app(self, app: Flask) -> None:
        raise NotImplementedError("TODO")


counter = Counter()


def create_app(config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    # TODO: configuration, blueprints and extension
    return app
