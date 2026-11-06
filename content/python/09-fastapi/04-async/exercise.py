"""Async in FastAPI.

1. async fetch_price(client, product) → float
     GET /prices/{product} with the AsyncClient; return json["price"].
2. async prices_in_parallel(client, products) → dict product → price
     All requests AT THE SAME TIME (asyncio.gather). The tests measure the time.
3. async with_timeout(coroutine, seconds) → the result, or None if it takes longer (asyncio.timeout).
4. GET /quote?products=a&products=b  (async endpoint)
     → {"total": sum of prices, "prices": {...}} using the client from get_client (Depends).
5. POST /orders  body {"email": str, "products": [str]}
     → 201 {"id": n} and adds send_confirmation(email, id) with BackgroundTasks.
"""

import asyncio  # noqa: F401
from collections.abc import AsyncIterator, Coroutine
from typing import Annotated, Any  # noqa: F401

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Query  # noqa: F401
from pydantic import BaseModel

PRICES_API = "https://api.prices.test"
SENT: list[tuple[str, int]] = []
ORDERS: list[dict[str, Any]] = []


async def get_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url=PRICES_API, timeout=5) as client:
        yield client


def send_confirmation(email: str, order_id: int) -> None:
    SENT.append((email, order_id))


class Order(BaseModel):
    email: str
    products: list[str]


async def fetch_price(client: httpx.AsyncClient, product: str) -> float:
    raise NotImplementedError("TODO")


async def prices_in_parallel(
    client: httpx.AsyncClient, products: list[str]
) -> dict[str, float]:
    raise NotImplementedError("TODO")


async def with_timeout(coroutine: Coroutine[Any, Any, Any], seconds: float) -> Any:
    raise NotImplementedError("TODO")


app = FastAPI()
