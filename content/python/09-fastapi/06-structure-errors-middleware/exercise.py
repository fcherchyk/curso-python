"""Estructura, errores y middleware.

Armá create_app() con:

1. lifespan: al arrancar, app.state.stock = copia de STOCK_INICIAL.
2. router = APIRouter(prefix="/productos", tags=["productos"]), incluido con prefix="/api/v1":
     GET  /api/v1/productos/{nombre}            → {"nombre", "stock"}
     POST /api/v1/productos/{nombre}/ventas     → body Venta {"cantidad": int > 0}
                                                  → {"nombre", "stock"} actualizado
   Usá vender() (lógica de dominio), que levanta las excepciones de abajo.
3. Handlers:
     ProductoNoEncontrado → 404 {"error": "producto_no_encontrado", "nombre": ...}
     StockInsuficiente    → 409 {"error": "stock_insuficiente", "disponible": ...}
     RequestValidationError → 422 {"error": "validacion", "campos": ["cantidad", ...]}
       (cada campo es el loc sin el primer elemento, unido con ".")
4. Middleware HTTP: header X-Request-ID (el que vino en el request o uuid4().hex)
   y X-Tiempo-Proceso (segundos, como string) en TODAS las respuestas.
"""

import time  # noqa: F401
import uuid  # noqa: F401
from contextlib import asynccontextmanager  # noqa: F401

from fastapi import APIRouter, FastAPI, Request  # noqa: F401
from fastapi.exceptions import RequestValidationError  # noqa: F401
from fastapi.responses import JSONResponse  # noqa: F401
from pydantic import BaseModel, Field

STOCK_INICIAL = {"yerba": 10, "cafe": 2}


class ProductoNoEncontrado(Exception):
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre


class StockInsuficiente(Exception):
    def __init__(self, disponible: int) -> None:
        self.disponible = disponible


def vender(stock: dict[str, int], nombre: str, cantidad: int) -> int:
    """Lógica de dominio (ya hecha): descuenta y devuelve el stock restante."""
    if nombre not in stock:
        raise ProductoNoEncontrado(nombre)
    if cantidad > stock[nombre]:
        raise StockInsuficiente(stock[nombre])
    stock[nombre] -= cantidad
    return stock[nombre]


class Venta(BaseModel):
    cantidad: int = Field(gt=0)


router = APIRouter(prefix="/productos", tags=["productos"])


def create_app() -> FastAPI:
    app = FastAPI()
    # TODO: lifespan, router, handlers y middleware
    return app
