import asyncio
from collections.abc import AsyncIterator, Coroutine
from typing import Annotated, Any

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Query
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
    r = await client.get(f"/prices/{product}")
    r.raise_for_status()
    return float(r.json()["price"])


async def prices_in_parallel(
    client: httpx.AsyncClient, products: list[str]
) -> dict[str, float]:
    prices = await asyncio.gather(*(fetch_price(client, p) for p in products))
    return dict(zip(products, prices, strict=True))


async def with_timeout(coroutine: Coroutine[Any, Any, Any], seconds: float) -> Any:
    try:
        async with asyncio.timeout(seconds):
            return await coroutine
    except TimeoutError:
        return None


app = FastAPI()
Client = Annotated[httpx.AsyncClient, Depends(get_client)]


@app.get("/quote")
async def quote(client: Client, products: Annotated[list[str], Query()]) -> dict[str, Any]:
    prices = await prices_in_parallel(client, products)
    return {"total": sum(prices.values()), "prices": prices}


@app.post("/orders", status_code=201)
def create_order(order: Order, tasks: BackgroundTasks) -> dict[str, int]:
    order_id = len(ORDERS) + 1
    ORDERS.append({"id": order_id, **order.model_dump()})
    tasks.add_task(send_confirmation, order.email, order_id)
    return {"id": order_id}
