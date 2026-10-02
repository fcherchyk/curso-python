# Estructura, errores y middleware

Una API de verdad no entra en un solo archivo. Este capítulo cierra el módulo con las piezas
de un proyecto FastAPI profesional: **routers** para organizar, **excepciones de dominio**
convertidas en respuestas HTTP coherentes, **middleware** para lo transversal (tiempos, ids de
request, CORS), el **lifespan** para inicializar recursos y una factory que deja todo testeable.

## Routers: los blueprints de FastAPI

```python
# app/routers/productos.py
from fastapi import APIRouter

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("")
def listar(): ...

@router.get("/{id}")
def detalle(id: int): ...
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import productos, usuarios

app = FastAPI()
app.include_router(productos.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
```

- `prefix` y `tags` se definen en el router o al incluirlo (y se acumulan).
- También se pueden agregar dependencias a todo un router:
  `APIRouter(dependencies=[Depends(usuario_actual)])`.
- Estructura típica: `routers/` (HTTP), `schemas/` (Pydantic), `models/` (ORM), `services/`
  (lógica de negocio) y `deps.py` (dependencias).

## Errores: excepciones de dominio y handlers

La lógica de negocio no debería saber de HTTP. Levanta **sus** excepciones y la capa web las
traduce:

```python
class ProductoNoEncontrado(Exception):
    def __init__(self, id: int):
        self.id = id

@app.exception_handler(ProductoNoEncontrado)
async def manejar_no_encontrado(request: Request, exc: ProductoNoEncontrado):
    return JSONResponse(
        status_code=404,
        content={"error": "producto_no_encontrado", "id": exc.id},
    )
```

Así, `services.vender(id, cantidad)` levanta `ProductoNoEncontrado` o `StockInsuficiente` y
cualquier endpoint que lo llame responde 404 o 409 sin `try/except`.

### Personalizar el 422

Los errores de validación de FastAPI son detallados pero verbosos. Si tu API tiene un formato de
error propio, se reemplaza el handler de `RequestValidationError`:

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validacion(request: Request, exc: RequestValidationError):
    campos = [".".join(str(p) for p in e["loc"][1:]) for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": "validacion", "campos": campos})
```

**Elegí un formato de error y usalo en todas partes.** Quien consume la API lo agradece. Hay un
estándar, *Problem Details* (RFC 9457), que muchas APIs adoptan.

## Middleware: código alrededor de cada request

```python
import time, uuid

@app.middleware("http")
async def medir_y_etiquetar(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    inicio = time.perf_counter()
    respuesta = await call_next(request)          # ejecuta la ruta (y otros middlewares)
    respuesta.headers["X-Request-ID"] = request_id
    respuesta.headers["X-Tiempo-Proceso"] = f"{time.perf_counter() - inicio:.4f}"
    return respuesta
```

- Lo que va **antes** de `call_next` corre antes de la ruta; lo que va **después**, con la
  respuesta ya armada.
- Usos típicos: logging y métricas, ids de correlación, headers de seguridad y compresión.
- Middlewares incluidos: `CORSMiddleware` (para que un frontend en otro dominio pueda llamar a
  tu API), `GZipMiddleware` y `TrustedHostMiddleware`.

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["https://mi-front.com"], allow_methods=["*"])
```

¿Middleware o dependencia? Si aplica a **todos** los requests y no necesita datos del endpoint,
middleware. Si es por endpoint o por router, o produce un valor (el usuario), dependencia.

## Lifespan: inicializar y liberar recursos

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cliente_http = httpx.AsyncClient()     # al arrancar
    app.state.cache = {}
    yield
    await app.state.cliente_http.aclose()            # al apagar

app = FastAPI(lifespan=lifespan)
```

`app.state` guarda recursos compartidos de **esa** app. Desde un endpoint se accede con
`request.app.state`. Reemplaza a los viejos `@app.on_event("startup")`. En los tests, el lifespan
corre usando `TestClient` como context manager: `with TestClient(app) as c: ...`.

## La factory

```python
def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(productos.router, prefix="/api/v1")
    app.add_exception_handler(ProductoNoEncontrado, manejar_no_encontrado)
    app.middleware("http")(medir_y_etiquetar)
    return app
```

Igual que en Flask: cada test arma su app limpia y no queda estado compartido.

## Despliegue, en dos líneas

En producción: `fastapi run app/main.py` o `uvicorn app.main:app --workers 4` (o `gunicorn` con
workers de uvicorn), detrás de un proxy (nginx o el balanceador de la nube), en un contenedor y
con la configuración por variables de entorno.

## Resumen

- `APIRouter(prefix, tags)` + `include_router` para organizar por recurso.
- Excepciones de dominio + `exception_handler` para que los errores sean coherentes; reemplazá el
  handler del 422 si tenés un formato propio.
- `@app.middleware("http")` para lo transversal; CORS con `CORSMiddleware`.
- `lifespan` y `app.state` para los recursos compartidos.
- Factory `create_app()` para los tests.

## Ejercicio

Una API de inventario armada con un router, excepciones de dominio con handlers, un formato
propio para el 422, un middleware de ids y tiempos, y un lifespan que carga el estado inicial.

**Para profundizar:** [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/),
[Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/),
[Middleware](https://fastapi.tiangolo.com/tutorial/middleware/),
[Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
