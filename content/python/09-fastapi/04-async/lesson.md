# Async in FastAPI

FastAPI is an **ASGI** framework: it can serve many requests at once on a single thread using
`async`/`await`. This matters when your endpoints **wait** on slow things, like calls to other
APIs, database queries or file reads. This chapter gives you just enough `asyncio` to use it
well on the web (the concurrency module goes deeper) and explains the most important rule:
**when to use `async def` and when to use `def`**.

## The problem: waiting without blocking

An endpoint that queries three external APIs of 200 ms each, one after another, takes 600 ms.
And while it waits on the network, **the process does nothing useful**. With async, while one
operation waits, the *event loop* handles others: other requests or other calls from the same
request.

## `async def` and `await`

```python
import asyncio

async def find_price(product: str) -> float:
    await asyncio.sleep(0.2)          # simulates waiting on the network
    return 100.0

async def main():
    price = await find_price("mate")  # await: "wait for this without blocking the loop"

asyncio.run(main())                   # entry point from synchronous code
```

- An `async def` function is a **coroutine**: calling it **doesn't run it**, it returns an
  object you have to wait on with `await` (like the generators from module 03, which don't run
  until you iterate them).
- `await` can only be used inside `async def`.
- `asyncio.run(...)` starts the loop. In FastAPI you don't need it: the server (uvicorn)
  already has one.

## Concurrency: `asyncio.gather`

```python
async def quote(products: list[str]) -> list[float]:
    return await asyncio.gather(*(find_price(p) for p in products))
```

`gather` launches all the coroutines **at once** and waits for all of them to finish. Three
200 ms waits take about 200 ms in total, not 600. It returns the results **in the order they
were passed in**.

Since 3.11 there's also `asyncio.TaskGroup`, which is safer with errors: if one task fails, it
cancels the rest and raises an `ExceptionGroup`, the one from module 06.

### Timeouts

```python
try:
    async with asyncio.timeout(2):           # 3.11+
        data = await slow_query()
except TimeoutError:
    data = None
```

On the web, **every external call should have a timeout**: otherwise, a service that's down
leaves you with requests hanging forever.

## Async HTTP: `httpx.AsyncClient`

`requests` is synchronous. For HTTP calls inside async code, use **httpx**, which has the same
API in both flavors:

```python
import httpx

async with httpx.AsyncClient(base_url="https://api.prices.test", timeout=5) as client:
    r = await client.get("/prices/mate")
    r.raise_for_status()                    # raises if the status is 4xx/5xx
    price = r.json()["price"]
```

Reuse the client (in a dependency or in the app's *lifespan*): creating one per request wastes
connections.

## The golden rule in FastAPI: `async def` vs. `def`

```python
@app.get("/a")
async def a():                # runs ON the event loop
    data = await client.get(...)        # ✓ async waits
    return data

@app.get("/b")
def b():                      # FastAPI runs it in a THREAD POOL
    return requests.get(...).json()     # ✓ blocks a thread, not the loop

@app.get("/c")
async def c():
    time.sleep(2)             # ✗✗ blocks the loop: the ENTIRE app freezes for 2 seconds!
    return requests.get(...)  # ✗✗ same thing
```

- Use **`async def`** if inside it you **only** use async libraries (`await httpx...`, async
  drivers).
- Use **`def`** if you use **synchronous** libraries (sync SQLAlchemy, `requests`,
  computations). FastAPI runs them in a thread pool, so they don't hold up everything else.
- **Never** call blocking code (`time.sleep`, `requests`, heavy file I/O) inside an
  `async def`. It's the most common mistake with FastAPI. If you have no alternative, use
  `await asyncio.to_thread(blocking_function, ...)`.

Dependencies follow the same rule: they can be `def` or `async def`.

## Background tasks: `BackgroundTasks`

For things that shouldn't delay the response (sending an email, writing an audit log):

```python
from fastapi import BackgroundTasks

def send_confirmation(email: str, order_id: int) -> None: ...

@app.post("/orders", status_code=201)
def create(order: Order, tasks: BackgroundTasks):
    order_id = save(order)
    tasks.add_task(send_confirmation, order.email, order_id)   # runs AFTER responding
    return {"id": order_id}
```

They're meant for short tasks. If you need retries or heavy processing, use a real queue
(Celery, RQ, Arq).

## Testing async code

`TestClient` handles async endpoints by itself, so your tests can be synchronous. To test
standalone `async` functions, `asyncio.run(...)` inside the test is enough (or use the
`pytest-asyncio` plugin). To simulate an external API, use `httpx.MockTransport`:

```python
async def handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"price": 100})

client = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="http://x")
```

## In the other frameworks

- **Flask** is WSGI and synchronous. It supports `async def` views, but each request still
  takes up a worker. For lots of concurrent I/O, you scale with more processes or threads.
- **Django** has had async views and an ORM with async methods (`aget`, `afilter`…) since
  version 4.x, although much of the ecosystem is still synchronous.

## Summary

- `async def` defines a coroutine; `await` waits without blocking the loop; `asyncio.run`
  starts it from sync code.
- `asyncio.gather` for concurrency (and `TaskGroup` in 3.11+); `asyncio.timeout` to cut it off.
- `httpx.AsyncClient` for async HTTP; reuse it.
- In FastAPI: `async def` only with async libraries; `def` with sync libraries; **never** block
  inside `async def`.
- `BackgroundTasks` for short tasks after responding.

## Exercise

Fetch prices from an external API in parallel (the tests check that it's **really**
concurrent by measuring the time), a timeout, an async endpoint with the injected HTTP client
and a background task.

**Further reading:** [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/),
[asyncio](https://docs.python.org/3/library/asyncio.html), [HTTPX Async](https://www.python-httpx.org/async/).
