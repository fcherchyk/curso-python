"""Structure, errors and middleware.

Build create_app() with:

1. lifespan: on startup, app.state.stock = copy of INITIAL_STOCK.
2. router = APIRouter(prefix="/products", tags=["products"]), included with prefix="/api/v1":
     GET  /api/v1/products/{name}               → {"name", "stock"}
     POST /api/v1/products/{name}/sales         → body Sale {"quantity": int > 0}
                                                  → updated {"name", "stock"}
   Use sell() (domain logic), which raises the exceptions below.
3. Handlers:
     ProductNotFound   → 404 {"error": "product_not_found", "name": ...}
     InsufficientStock → 409 {"error": "insufficient_stock", "available": ...}
     RequestValidationError → 422 {"error": "validation", "fields": ["quantity", ...]}
       (each field is the loc without its first element, joined with ".")
4. HTTP middleware: header X-Request-ID (the one sent in the request, or uuid4().hex)
   and X-Process-Time (seconds, as a string) on ALL responses.
"""

import time  # noqa: F401
import uuid  # noqa: F401
from contextlib import asynccontextmanager  # noqa: F401

from fastapi import APIRouter, FastAPI, Request  # noqa: F401
from fastapi.exceptions import RequestValidationError  # noqa: F401
from fastapi.responses import JSONResponse  # noqa: F401
from pydantic import BaseModel, Field

INITIAL_STOCK = {"mate": 10, "coffee": 2}


class ProductNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


class InsufficientStock(Exception):
    def __init__(self, available: int) -> None:
        self.available = available


def sell(stock: dict[str, int], name: str, quantity: int) -> int:
    """Domain logic (already done): subtracts and returns the remaining stock."""
    if name not in stock:
        raise ProductNotFound(name)
    if quantity > stock[name]:
        raise InsufficientStock(stock[name])
    stock[name] -= quantity
    return stock[name]


class Sale(BaseModel):
    quantity: int = Field(gt=0)


router = APIRouter(prefix="/products", tags=["products"])


def create_app() -> FastAPI:
    app = FastAPI()
    # TODO: lifespan, router, handlers and middleware
    return app
