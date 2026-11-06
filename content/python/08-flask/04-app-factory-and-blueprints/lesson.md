# App factory and blueprints

In the previous chapters the app was a global variable: `app = Flask(__name__)`. That's fine for
getting started, but it has real problems. You can't create two apps with different
configurations (one for tests and another for production), imports become circular as the project
grows, and every route ends up in a single file. The standard Flask solution combines two
patterns: the **app factory** and **blueprints**.

## App factory: a function that creates the app

```python
# store/__init__.py
from flask import Flask

def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        ENVIRONMENT="development",
        DATABASE_URL="sqlite:///store.db",
    )
    if config:
        app.config.update(config)          # whatever you pass overrides the defaults

    from store import api, web             # imports inside: avoids cycles
    app.register_blueprint(api.bp, url_prefix="/api")
    app.register_blueprint(web.bp)

    db.init_app(app)                       # extensions
    return app
```

```bash
uv run flask --app "store:create_app()" run
```

Advantages:

- **Isolated tests**: each test creates its own app with `create_app({"TESTING": True, ...})`.
- **Multiple configurations** (development, tests, production) without touching the code.
- **No global state** shared between apps.

### Configuration

```python
app.config["SECRET_KEY"]                         # it's a dict
app.config.from_mapping(KEY=value)
app.config.from_prefixed_env()                   # reads FLASK_* from the environment: FLASK_SECRET_KEY → SECRET_KEY
app.config.from_object("store.config.Production")
```

Keys are UPPERCASE. Secrets come **from the environment**, never from the repository.

## `current_app`: the "current" app

If the app is created inside a function, how does a view access the configuration? With
`current_app`, a proxy to the app handling the request:

```python
from flask import current_app

@bp.get("/status")
def status():
    return {"environment": current_app.config["ENVIRONMENT"]}
```

Along with `request`, `session` and `g`, it's part of Flask's **contexts**. Outside a request (in
a script or a test), you need to push a context: `with app.app_context(): ...`.

## Blueprints: grouping routes

A blueprint is a "module of routes" that gets registered on the app later:

```python
# store/api.py
from flask import Blueprint

bp = Blueprint("api", __name__)

@bp.get("/products")
def products():
    ...
```

```python
app.register_blueprint(bp, url_prefix="/api")    # → GET /api/products
```

- Each blueprint has a **name**, used as the prefix of its endpoints in `url_for`:
  `url_for("api.products")`. Inside the same blueprint, `url_for(".products")`.
- It can have its own templates, static files, error handlers and hooks (`@bp.before_request`).
- The usual approach is one blueprint per area: `auth`, `api`, `admin`, `web`.

## Extensions: the `init_app` pattern

Extensions (Flask-SQLAlchemy, Flask-Login, Flask-Migrate…) are created **without an app** and
attached later, inside the factory:

```python
# store/extensions.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()            # no app: can be imported from anywhere

# in create_app
db.init_app(app)
```

If you write your own extension, follow the same pattern: store the state in
`app.extensions["name"]`, never on the extension object, because there may be several apps.

```python
class Counter:
    def init_app(self, app):
        app.extensions["counter"] = {"visits": 0}

        @app.before_request
        def count():
            app.extensions["counter"]["visits"] += 1
```

## Testing with the factory

```python
import pytest
from store import create_app

@pytest.fixture
def app():
    return create_app({"TESTING": True, "DATABASE_URL": "sqlite://"})

@pytest.fixture
def client(app):
    return app.test_client()

def test_status(client):
    assert client.get("/api/status").get_json()["environment"] == "development"
```

`TESTING=True` makes exceptions propagate to the test instead of becoming a 500.

## In the other frameworks

- **FastAPI**: `APIRouter` plays the role of blueprints (`app.include_router(router,
  prefix="/api")`), and you can also use a factory function.
- **Django** comes organized this way out of the box: a project with several **apps**, each with
  its own `urls.py`, wired in with `include()`; configuration lives in `settings.py`.

## Summary

- `create_app(config)` creates and configures the app; no global `app` in real projects.
- `app.config` in uppercase, with secrets from the environment.
- `current_app` to reach the current app from views.
- Blueprints to group routes by area; `url_for("blueprint.view")`.
- Extensions without an app + `init_app(app)` in the factory; state goes in `app.extensions`.

## Exercise

A factory with default configuration and overrides, two blueprints (`api` with a prefix and `web`)
and a minimal extension with `init_app`.

**Further reading:** [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/),
[Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/),
[Flask Extension Development](https://flask.palletsprojects.com/en/stable/extensiondev/).
