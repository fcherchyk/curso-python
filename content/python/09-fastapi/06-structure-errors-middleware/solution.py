import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

INITIAL_STOCK = {"mate": 10, "coffee": 2}


class ProductNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


class InsufficientStock(Exception):
    def __init__(self, available: int) -> None:
        self.available = available


def sell(stock: dict[str, int], name: str, quantity: int) -> int:
    if name not in stock:
        raise ProductNotFound(name)
    if quantity > stock[name]:
        raise InsufficientStock(stock[name])
    stock[name] -= quantity
    return stock[name]


class Sale(BaseModel):
    quantity: int = Field(gt=0)


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/{name}")
def detail(name: str, request: Request) -> dict[str, object]:
    stock = request.app.state.stock
    if name not in stock:
        raise ProductNotFound(name)
    return {"name": name, "stock": stock[name]}


@router.post("/{name}/sales")
def record_sale(name: str, sale: Sale, request: Request) -> dict[str, object]:
    remaining = sell(request.app.state.stock, name, sale.quantity)
    return {"name": name, "stock": remaining}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.stock = dict(INITIAL_STOCK)  # copy: each app starts with its own state
    yield


async def not_found(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, ProductNotFound)
    return JSONResponse(
        status_code=404, content={"error": "product_not_found", "name": exc.name}
    )


async def out_of_stock(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, InsufficientStock)
    return JSONResponse(
        status_code=409, content={"error": "insufficient_stock", "available": exc.available}
    )


async def validation(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    fields = [".".join(str(p) for p in e["loc"][1:]) for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": "validation", "fields": fields})


async def tag_request(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router, prefix="/api/v1")
    app.add_exception_handler(ProductNotFound, not_found)
    app.add_exception_handler(InsufficientStock, out_of_stock)
    app.add_exception_handler(RequestValidationError, validation)
    app.middleware("http")(tag_request)
    return app
