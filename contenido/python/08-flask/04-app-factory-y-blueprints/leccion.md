# App factory y blueprints

En los capítulos anteriores la app era una variable global: `app = Flask(__name__)`. Sirve para
empezar, pero tiene problemas reales. No podés crear dos apps con configuraciones distintas
(una para tests y otra para producción), los imports se vuelven circulares cuando el proyecto
crece y todas las rutas terminan en un solo archivo. La solución estándar en Flask combina dos
patrones: la **app factory** y los **blueprints**.

## App factory: una función que crea la app

```python
# tienda/__init__.py
from flask import Flask

def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        ENTORNO="desarrollo",
        DATABASE_URL="sqlite:///tienda.db",
    )
    if config:
        app.config.update(config)          # lo que pasás pisa los defaults

    from tienda import api, web            # imports adentro: evita ciclos
    app.register_blueprint(api.bp, url_prefix="/api")
    app.register_blueprint(web.bp)

    db.init_app(app)                       # extensiones
    return app
```

```bash
uv run flask --app "tienda:create_app()" run
```

Ventajas:

- **Tests aislados**: cada test crea su propia app con `create_app({"TESTING": True, ...})`.
- **Varias configuraciones** (desarrollo, tests, producción) sin tocar el código.
- **Sin estado global** compartido entre apps.

### Configuración

```python
app.config["SECRET_KEY"]                         # es un dict
app.config.from_mapping(CLAVE=valor)
app.config.from_prefixed_env()                   # lee FLASK_* del entorno: FLASK_SECRET_KEY → SECRET_KEY
app.config.from_object("tienda.config.Produccion")
```

Las claves van en MAYÚSCULAS. Los secretos vienen **del entorno**, nunca del repositorio.

## `current_app`: la app "actual"

Si la app se crea en una función, ¿cómo accede una vista a la configuración? Con `current_app`,
un proxy a la app que está atendiendo el request:

```python
from flask import current_app

@bp.get("/estado")
def estado():
    return {"entorno": current_app.config["ENTORNO"]}
```

Junto con `request`, `session` y `g`, forma parte de los **contextos** de Flask. Fuera de un
request (en un script o en un test), hace falta abrir un contexto: `with app.app_context(): ...`.

## Blueprints: agrupar rutas

Un blueprint es un "módulo de rutas" que se registra en la app más tarde:

```python
# tienda/api.py
from flask import Blueprint

bp = Blueprint("api", __name__)

@bp.get("/productos")
def productos():
    ...
```

```python
app.register_blueprint(bp, url_prefix="/api")    # → GET /api/productos
```

- Cada blueprint tiene un **nombre**, que se usa como prefijo de sus endpoints en `url_for`:
  `url_for("api.productos")`. Dentro del mismo blueprint, `url_for(".productos")`.
- Puede tener sus propias plantillas, archivos estáticos, error handlers y hooks
  (`@bp.before_request`).
- Lo habitual es un blueprint por área: `auth`, `api`, `admin`, `web`.

## Extensiones: el patrón `init_app`

Las extensiones (Flask-SQLAlchemy, Flask-Login, Flask-Migrate…) se crean **sin app** y se
conectan después, dentro de la factory:

```python
# tienda/extensiones.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()            # sin app: se puede importar desde cualquier lado

# en create_app
db.init_app(app)
```

Si escribís tu propia extensión, seguís el mismo patrón: guardás el estado en
`app.extensions["nombre"]`, nunca en el objeto de la extensión, porque puede haber varias apps.

```python
class Contador:
    def init_app(self, app):
        app.extensions["contador"] = {"visitas": 0}

        @app.before_request
        def contar():
            app.extensions["contador"]["visitas"] += 1
```

## Testear con la factory

```python
import pytest
from tienda import create_app

@pytest.fixture
def app():
    return create_app({"TESTING": True, "DATABASE_URL": "sqlite://"})

@pytest.fixture
def cliente(app):
    return app.test_client()

def test_estado(cliente):
    assert cliente.get("/api/estado").get_json()["entorno"] == "desarrollo"
```

`TESTING=True` hace que las excepciones se propaguen al test en lugar de convertirse en un 500.

## En los otros frameworks

- **FastAPI**: `APIRouter` cumple el rol de los blueprints (`app.include_router(router,
  prefix="/api")`), y también se puede usar una función factory.
- **Django** viene organizado así de fábrica: un proyecto con varias **apps**, cada una con sus
  `urls.py`, que se incluyen con `include()`; la configuración vive en `settings.py`.

## Resumen

- `create_app(config)` crea y configura la app; nada de `app` global en proyectos reales.
- `app.config` en mayúsculas, con los secretos desde el entorno.
- `current_app` para acceder a la app actual desde las vistas.
- Blueprints para agrupar rutas por área; `url_for("blueprint.vista")`.
- Extensiones sin app + `init_app(app)` en la factory; el estado va en `app.extensions`.

## Ejercicio

Una factory con configuración por defecto y overrides, dos blueprints (`api` con prefijo y `web`)
y una extensión mínima con `init_app`.

**Para profundizar:** [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/),
[Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/),
[Flask Extension Development](https://flask.palletsprojects.com/en/stable/extensiondev/).
