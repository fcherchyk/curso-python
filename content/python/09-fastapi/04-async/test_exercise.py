import asyncio
import time

import exercise
import httpx
import pytest
from exercise import (
    app,
    fetch_price,
    get_client,
    prices_in_parallel,
    with_timeout,
)
from fastapi.testclient import TestClient

PRICES = {"mate": 3500.0, "coffee": 9800.0, "tea": 1200.0, "sugar": 900.0, "milk": 1500.0}
DELAY = 0.2


async def fake_api(request: httpx.Request) -> httpx.Response:
    await asyncio.sleep(DELAY)  # each request "takes" 200 ms
    product = request.url.path.rsplit("/", 1)[-1]
    if product not in PRICES:
        return httpx.Response(404, json={"error": "not found"})
    return httpx.Response(200, json={"price": PRICES[product]})


def fake_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(fake_api), base_url="http://fake")


def test_fetch_price():
    async def case():
        async with fake_client() as c:
            return await fetch_price(c, "mate")

    assert asyncio.run(case()) == 3500.0


def test_prices_in_parallel_is_concurrent():
    async def case():
        async with fake_client() as c:
            start = time.perf_counter()
            res = await prices_in_parallel(c, list(PRICES))
            return res, time.perf_counter() - start

    res, elapsed = asyncio.run(case())
    assert res == PRICES
    assert elapsed < DELAY * 2.5, f"took {elapsed:.2f}s: are the requests running one by one?"


def test_with_timeout():
    async def slow():
        await asyncio.sleep(1)
        return "late"

    async def fast():
        return "ok"

    assert asyncio.run(with_timeout(fast(), 0.5)) == "ok"
    start = time.perf_counter()
    assert asyncio.run(with_timeout(slow(), 0.1)) is None
    assert time.perf_counter() - start < 0.5


@pytest.fixture
def client():
    async def override():
        async with fake_client() as c:
            yield c

    app.dependency_overrides[get_client] = override
    exercise.SENT.clear()
    exercise.ORDERS.clear()
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_quote_endpoint(client):
    start = time.perf_counter()
    r = client.get("/quote", params={"products": ["mate", "coffee", "tea"]})
    assert r.status_code == 200
    assert r.json() == {
        "total": 14500.0,
        "prices": {"mate": 3500.0, "coffee": 9800.0, "tea": 1200.0},
    }
    assert time.perf_counter() - start < DELAY * 2.5, "the endpoint must be concurrent too"


def test_order_with_background_task(client):
    r = client.post("/orders", json={"email": "alice@x.com", "products": ["mate"]})
    assert r.status_code == 201
    assert r.json() == {"id": 1}
    assert exercise.SENT == [("alice@x.com", 1)]
