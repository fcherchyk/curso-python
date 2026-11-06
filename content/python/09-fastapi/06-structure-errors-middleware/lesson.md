# Structure, errors and middleware

A real API doesn't fit in a single file. This chapter wraps up the module with the pieces of a
professional FastAPI project: **routers** to organize, **domain exceptions** turned into
consistent HTTP responses, **middleware** for cross-cutting concerns (timing, request ids,
CORS), the **lifespan** to initialize resources, and a factory that keeps everything testable.

## Routers: FastAPI's blueprints

```python
# app/routers/products.py
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

@router.get("")
def list_products(): ...

@router.get("/{id}")
def detail(id: int): ...
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import products, users

app = FastAPI()
app.include_router(products.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
```

- `prefix` and `tags` are set on the router or when including it (and they stack up).
- You can also add dependencies to an entire router:
  `APIRouter(dependencies=[Depends(current_user)])`.
- Typical layout: `routers/` (HTTP), `schemas/` (Pydantic), `models/` (ORM), `services/`
  (business logic) and `deps.py` (dependencies).

## Errors: domain exceptions and handlers

Business logic shouldn't know about HTTP. It raises **its own** exceptions and the web layer
translates them:

```python
class ProductNotFound(Exception):
    def __init__(self, id: int):
        self.id = id

@app.exception_handler(ProductNotFound)
async def handle_not_found(request: Request, exc: ProductNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": "product_not_found", "id": exc.id},
    )
```

That way, `services.sell(id, quantity)` raises `ProductNotFound` or `InsufficientStock`, and
any endpoint that calls it responds 404 or 409 without a `try/except`.

### Customizing the 422

FastAPI's validation errors are detailed but verbose. If your API has its own error format,
replace the `RequestValidationError` handler:

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation(request: Request, exc: RequestValidationError):
    fields = [".".join(str(p) for p in e["loc"][1:]) for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": "validation", "fields": fields})
```

**Pick one error format and use it everywhere.** Whoever consumes your API will thank you.
There's a standard, *Problem Details* (RFC 9457), that many APIs adopt.

## Middleware: code around every request

```python
import time, uuid

@app.middleware("http")
async def time_and_tag(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    start = time.perf_counter()
    response = await call_next(request)           # runs the route (and other middlewares)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    return response
```

- What goes **before** `call_next` runs before the route; what goes **after** runs with the
  response already built.
- Typical uses: logging and metrics, correlation ids, security headers and compression.
- Built-in middlewares: `CORSMiddleware` (so a frontend on another domain can call your API),
  `GZipMiddleware` and `TrustedHostMiddleware`.

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["https://my-frontend.com"], allow_methods=["*"])
```

Middleware or dependency? If it applies to **every** request and doesn't need data from the
endpoint, middleware. If it's per endpoint or per router, or it produces a value (the user),
dependency.

## Lifespan: initializing and releasing resources

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient()      # on startup
    app.state.cache = {}
    yield
    await app.state.http_client.aclose()             # on shutdown

app = FastAPI(lifespan=lifespan)
```

`app.state` holds shared resources for **that** app. From an endpoint you reach it with
`request.app.state`. It replaces the old `@app.on_event("startup")`. In tests, the lifespan
runs when you use `TestClient` as a context manager: `with TestClient(app) as c: ...`.

## The factory

```python
def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(products.router, prefix="/api/v1")
    app.add_exception_handler(ProductNotFound, handle_not_found)
    app.middleware("http")(time_and_tag)
    return app
```

Same as in Flask: each test builds its own clean app and no state is shared.

## Deployment, in two lines

In production: `fastapi run app/main.py` or `uvicorn app.main:app --workers 4` (or `gunicorn`
with uvicorn workers), behind a proxy (nginx or the cloud load balancer), in a container and
configured through environment variables.

## Summary

- `APIRouter(prefix, tags)` + `include_router` to organize by resource.
- Domain exceptions + `exception_handler` for consistent errors; replace the 422 handler if you
  have your own format.
- `@app.middleware("http")` for cross-cutting concerns; CORS with `CORSMiddleware`.
- `lifespan` and `app.state` for shared resources.
- A `create_app()` factory for tests.

## Exercise

An inventory API built with a router, domain exceptions with handlers, a custom format for the
422, a middleware for ids and timing, and a lifespan that loads the initial state.

**Further reading:** [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/),
[Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/),
[Middleware](https://fastapi.tiangolo.com/tutorial/middleware/),
[Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
