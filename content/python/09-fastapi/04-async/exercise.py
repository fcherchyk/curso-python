"""Async en FastAPI.

1. async obtener_precio(cliente, producto) → float
     GET /precios/{producto} con el AsyncClient; devolvé json["precio"].
2. async precios_en_paralelo(cliente, productos) → dict producto → precio
     Todas las consultas A LA VEZ (asyncio.gather). Los tests miden el tiempo.
3. async con_timeout(corrutina, segundos) → el resultado, o None si tarda más (asyncio.timeout).
4. GET /cotizacion?productos=a&productos=b  (endpoint async)
     → {"total": suma de precios, "precios": {...}} usando el cliente de get_cliente (Depends).
5. POST /pedidos  body {"email": str, "productos": [str]}
     → 201 {"id": n} y agrega con BackgroundTasks enviar_confirmacion(email, id).
"""

import asyncio  # noqa: F401
from collections.abc import AsyncIterator, Coroutine
from typing import Annotated, Any  # noqa: F401

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Query  # noqa: F401
from pydantic import BaseModel

API_PRECIOS = "https://api.precios.test"
ENVIADOS: list[tuple[str, int]] = []
PEDIDOS: list[dict[str, Any]] = []


async def get_cliente() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url=API_PRECIOS, timeout=5) as cliente:
        yield cliente


def enviar_confirmacion(email: str, pedido_id: int) -> None:
    ENVIADOS.append((email, pedido_id))


class Pedido(BaseModel):
    email: str
    productos: list[str]


async def obtener_precio(cliente: httpx.AsyncClient, producto: str) -> float:
    raise NotImplementedError("TODO")


async def precios_en_paralelo(
    cliente: httpx.AsyncClient, productos: list[str]
) -> dict[str, float]:
    raise NotImplementedError("TODO")


async def con_timeout(corrutina: Coroutine[Any, Any, Any], segundos: float) -> Any:
    raise NotImplementedError("TODO")


app = FastAPI()
