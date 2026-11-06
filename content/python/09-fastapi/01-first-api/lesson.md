# FastAPI: your first API

FastAPI is the Python web framework that has grown the most in recent years. Its core idea is
to use the **type hints** you already write for everything: validating input data, converting
types, serializing responses and generating **interactive documentation** (OpenAPI)
automatically. It's built on **Starlette** (the web part, ASGI) and **Pydantic** (validation).
This very course app is built with FastAPI.

## The minimal app

```python
from fastapi import FastAPI

app = FastAPI(title="Store")

@app.get("/")
def home():
    return {"message": "Hello, FastAPI"}
```

```bash
uv add "fastapi[standard]"
uv run fastapi dev app.py       # http://127.0.0.1:8000  (or: uvicorn app:app --reload)
```

Open **`/docs`** and you'll see the interactive documentation (Swagger UI) generated from your
code, where you can try out every endpoint. `/redoc` has another view, and `/openapi.json` has
the raw schema.

## Path parameters: typed

```python
@app.get("/products/{id}")
def detail(id: int):
    return {"id": id}
```

- The variable is declared in the path with braces `{id}` and as a **function parameter**.
- The type hint **converts and validates**: `/products/7` calls with `id=7` (int), and
  `/products/abc` responds **422** with a JSON body explaining the error, without reaching your
  function.

Compare this with Flask, where the converter goes in the route (`<int:id>`) and data is read
from a global `request`. In FastAPI, **everything the function needs is in its signature**.

## Query parameters: the ones that aren't in the path

```python
@app.get("/products")
def list_products(q: str | None = None, page: int = 1, in_stock: bool = False):
    ...
```

```
GET /products?q=mate&page=2&in_stock=true
```

- Any simple-typed parameter that does **not** appear in the path is a **query param**.
- With a default it's optional; without one it's **required** (if missing, 422).
- `bool` accepts `true/false/1/0/yes/no/on/off`.
- For more validation, use `Query`: `page: Annotated[int, Query(ge=1)] = 1` requires it to be ≥ 1.

## Responses and status codes

```python
from fastapi import HTTPException, status

@app.get("/products/{id}")
def detail(id: int):
    product = PRODUCTS.get(id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return product            # dict, list or Pydantic model → JSON

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create(...):
    ...
```

- Whatever you return is serialized to JSON.
- `HTTPException` is **raised** (not returned), and FastAPI responds with
  `{"detail": "..."}` and the given status code.
- `status_code=` in the decorator sets the default success code.

## The body: with Pydantic (a preview)

To receive JSON in the body, you declare a **model**:

```python
from pydantic import BaseModel

class NewProduct(BaseModel):
    name: str
    price: int

@app.post("/products", status_code=201)
def create(data: NewProduct):           # a model as a parameter = the body
    ...
    return {"id": 3, **data.model_dump()}
```

If the JSON has no `name` or `price` isn't a number, FastAPI responds **422** detailing each
invalid field. No need to validate by hand like in Flask. The next chapter is all about
Pydantic.

## `def` or `async def`

Views can be `def` or `async def`, and FastAPI accepts both. For now, use `def`; in the async
chapter we'll see when each one makes sense.

## Testing with `TestClient`

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_detail():
    r = client.get("/products/1")
    assert r.status_code == 200
    assert r.json()["name"] == "mate"

def test_validation():
    assert client.get("/products/abc").status_code == 422
```

`TestClient` is based on `httpx`: same API (`get`, `post(json=...)`, `params=`,
`headers=`) and responses with `.json()`, `.text` and `.status_code`.

## Compared with Flask

| Flask                                  | FastAPI                                     |
|----------------------------------------|---------------------------------------------|
| `@app.get("/p/<int:id>")`              | `@app.get("/p/{id}")` + `id: int`           |
| `request.args.get("q", type=int)`      | parameter `q: int \| None = None`            |
| `request.get_json()` + manual checks   | parameter `data: Model` (automatic validation) |
| `return {...}, 404` or `abort(404)`    | `raise HTTPException(404, ...)`             |
| hand-made 400                          | automatic 422 with per-field details        |
| no documentation                       | automatic `/docs` (OpenAPI)                 |
| WSGI (synchronous)                     | ASGI (sync and async)                       |

## Summary

- `app = FastAPI()` and `@app.get/post/...` just like in Flask.
- Path parameters `{id}` + `id: int`; all other simple parameters are query params.
- Type hints validate and convert: invalid data gives a 422 with the details.
- `raise HTTPException(status_code, detail)` for errors; `status_code=` for the success code.
- `/docs` for free; `TestClient(app)` for testing.

## Exercise

The same products API from the first Flask chapter, now in FastAPI: you'll see how much
validation code disappears.

**Further reading:** [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/),
[Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/),
[Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/).
