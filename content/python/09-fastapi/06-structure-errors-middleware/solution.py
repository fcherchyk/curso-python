import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

STOCK_INICIAL = {"yerba": 10, "cafe": 2}


class ProductoNoEncontrado(Exception):
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre


class StockInsuficiente(Exception):
    def __init__(self, disponible: int) -> None:
        self.disponible = disponible


def vender(stock: dict[str, int], nombre: str, cantidad: int) -> int:
    if nombre not in stock:
        raise ProductoNoEncontrado(nombre)
    if cantidad > stock[nombre]:
        raise StockInsuficiente(stock[nombre])
    stock[nombre] -= cantidad
    return stock[nombre]


class Venta(BaseModel):
    cantidad: int = Field(gt=0)


router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/{nombre}")
def detalle(nombre: str, request: Request) -> dict[str, object]:
    stock = request.app.state.stock
    if nombre not in stock:
        raise ProductoNoEncontrado(nombre)
    return {"nombre": nombre, "stock": stock[nombre]}


@router.post("/{nombre}/ventas")
def registrar_venta(nombre: str, venta: Venta, request: Request) -> dict[str, object]:
    restante = vender(request.app.state.stock, nombre, venta.cantidad)
    return {"nombre": nombre, "stock": restante}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.stock = dict(STOCK_INICIAL)  # copia: cada app arranca con su estado
    yield


async def no_encontrado(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, ProductoNoEncontrado)
    return JSONResponse(
        status_code=404, content={"error": "producto_no_encontrado", "nombre": exc.nombre}
    )


async def sin_stock(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StockInsuficiente)
    return JSONResponse(
        status_code=409, content={"error": "stock_insuficiente", "disponible": exc.disponible}
    )


async def validacion(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    campos = [".".join(str(p) for p in e["loc"][1:]) for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": "validacion", "campos": campos})


async def etiquetar(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    inicio = time.perf_counter()
    respuesta = await call_next(request)
    respuesta.headers["X-Request-ID"] = request_id
    respuesta.headers["X-Tiempo-Proceso"] = f"{time.perf_counter() - inicio:.6f}"
    return respuesta


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router, prefix="/api/v1")
    app.add_exception_handler(ProductoNoEncontrado, no_encontrado)
    app.add_exception_handler(StockInsuficiente, sin_stock)
    app.add_exception_handler(RequestValidationError, validacion)
    app.middleware("http")(etiquetar)
    return app
