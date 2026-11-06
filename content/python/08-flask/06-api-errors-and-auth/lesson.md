# APIs REST: errores, autenticación y testing

Una API seria tiene que responder **siempre en JSON**, incluso cuando algo sale mal. También
tiene que proteger sus endpoints y estar cubierta por tests confiables. En este capítulo
armamos las tres piezas con Flask: error handlers globales, un decorador de autenticación por
token y el contexto `g`, y fixtures de pytest bien organizadas.

## Errores en JSON: `errorhandler`

Por defecto, `abort(404)` devuelve una página HTML. Para una API, se registra un handler:

```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def error_http(e: HTTPException):
    return {"error": e.name, "detalle": e.description}, e.code
```

Como todas las excepciones HTTP de Werkzeug heredan de `HTTPException`, con un solo handler
cubrís 400, 401, 403, 404, 405, etc., incluidas las rutas inexistentes y los métodos no
permitidos.

También se pueden mapear **excepciones de tu dominio** a códigos HTTP:

```python
class NoEncontrado(Exception): ...

@app.errorhandler(NoEncontrado)
def no_encontrado(e):
    return {"error": "Not Found", "detalle": str(e)}, 404

@app.errorhandler(ValueError)
def valor_invalido(e):
    return {"error": "Bad Request", "detalle": str(e)}, 400
```

Así la lógica de negocio levanta excepciones normales de Python y la capa HTTP decide cómo
responder. Es la misma idea que los `exception_handler` de FastAPI.

Para los errores 500, `@app.errorhandler(Exception)` atrapa todo lo demás: **logueá el
traceback** y devolvé un mensaje genérico, sin detalles internos. Con `TESTING=True`, Flask
deja que las excepciones lleguen al test para que veas el error real.

## Autenticación por token con un decorador

El patrón más simple para una API es un **token** en el header
`Authorization: Bearer <token>`:

```python
import functools
from flask import abort, current_app, g, request

def requiere_token(vista):
    @functools.wraps(vista)
    def envoltura(*args, **kwargs):
        encabezado = request.headers.get("Authorization", "")
        esquema, _, token = encabezado.partition(" ")
        if esquema != "Bearer" or not token:
            abort(401, description="falta el token")
        usuario = current_app.config["TOKENS"].get(token)
        if usuario is None:
            abort(401, description="token inválido")
        g.usuario = usuario                  # disponible durante este request
        return vista(*args, **kwargs)
    return envoltura

@app.get("/api/yo")
@requiere_token
def yo():
    return {"usuario": g.usuario}
```

- Es un **decorador** como los del módulo 04, y `functools.wraps` es imprescindible: Flask
  usa el nombre de la función como endpoint, y sin `wraps` dos vistas protegidas chocarían.
- El orden importa: `@app.get` va **arriba** (se aplica último), así se registra la versión ya
  protegida.
- `g` es un objeto "global" **por request**, para guardar datos que comparten las funciones de
  ese request, como el usuario autenticado o la conexión a la base.
- **401** significa "no sé quién sos" (falta la credencial o es inválida); **403**, "sé quién
  sos, pero no podés".

En producción, los tokens suelen ser **JWT** (firmados, con expiración) o tokens opacos
guardados en la base, y se comparan con `secrets.compare_digest` para evitar ataques de timing.
Para sesiones con login, **Flask-Login**.

## Fixtures de pytest para Flask

```python
# conftest.py
import pytest
from tienda import create_app

@pytest.fixture
def app():
    return create_app({"TESTING": True, "TOKENS": {"t-ana": "ana"}})

@pytest.fixture
def cliente(app):
    return app.test_client()

@pytest.fixture
def auth():
    return {"Authorization": "Bearer t-ana"}
```

```python
def test_yo(cliente, auth):
    assert cliente.get("/api/yo", headers=auth).get_json() == {"usuario": "ana"}

def test_yo_sin_token(cliente):
    r = cliente.get("/api/yo")
    assert r.status_code == 401
    assert r.get_json()["detalle"] == "falta el token"
```

Las fixtures se componen (`cliente` depende de `app`) y cada test recibe instancias nuevas.
Testeá **los casos de error con el mismo cuidado que el camino feliz**: son los que más se
rompen.

## Diseño REST en dos minutos

| Acción               | Método y ruta            | Respuesta típica         |
|----------------------|--------------------------|--------------------------|
| listar               | `GET /notas`             | 200 + lista              |
| detalle              | `GET /notas/7`           | 200 o 404                |
| crear                | `POST /notas`            | 201 + recurso creado     |
| reemplazar/modificar | `PUT`/`PATCH /notas/7`   | 200 o 204                |
| borrar               | `DELETE /notas/7`        | 204                      |

Las rutas son **sustantivos en plural**; la acción la da el método. Los errores tienen siempre
la misma forma (por ejemplo `{"error", "detalle"}`), así quien consume la API los maneja de
manera uniforme.

## En los otros frameworks

- **FastAPI** resuelve la autenticación con **dependencias** (`Depends(usuario_actual)`) en lugar
  de decoradores y valida el body automáticamente con Pydantic.
- **Django REST Framework** trae clases de autenticación y permisos (`IsAuthenticated`) y un
  formato de errores estándar.

## Resumen

- `@app.errorhandler(HTTPException)` para que todos los errores HTTP salgan en JSON.
- Mapeá excepciones de dominio a códigos HTTP con handlers propios.
- Autenticación con un decorador que lee `Authorization: Bearer ...`, guarda el usuario en `g` y
  usa `functools.wraps`.
- 401 = no autenticado; 403 = sin permiso.
- Fixtures `app` → `cliente` → `auth` en `conftest.py`; testeá también los errores.

## Ejercicio

Una API de notas con errores en JSON, un decorador de token y una excepción de dominio
mapeada a 400.

**Para profundizar:** [Handling Application Errors](https://flask.palletsprojects.com/en/stable/errorhandling/),
[View Decorators](https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/).
