# Flask: your first app

Flask is a **microframework**: it ships the bare minimum for handling HTTP requests (routing,
request and response, templates) and leaves everything else (database, forms, auth) to extensions
you pick yourself. It's simple, explicit and very easy to read, which makes it great both for small
APIs and for understanding what bigger frameworks do under the hood.

## The minimal app

```python
from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return "Hello, Flask!"
```

```bash
uv add flask
uv run flask --app app run --debug     # http://127.0.0.1:5000
```

- `Flask(__name__)` creates the application. It uses `__name__` to find templates and static
  files relative to the module.
- `@app.get("/")` registers the function as the **view** for that route and the GET method. It's a
  registration decorator, like the ones you saw in the functions module.
- Whatever the view returns becomes the response.
- `--debug` turns on auto-reload and the in-browser debugger. **Never in production**: it lets
  people run code.

## Routes and methods

```python
@app.get("/products")                  # shortcuts: get, post, put, patch, delete
def list_products(): ...

@app.post("/products")
def create(): ...

@app.route("/contact", methods=["GET", "POST"])   # general form
def contact(): ...
```

### Route variables and converters

```python
@app.get("/users/<name>")                  # string (no "/")
def profile(name): ...

@app.get("/products/<int:id>")             # converts to int; if it's not a number → 404
def detail(id): ...

@app.get("/files/<path:filepath>")         # allows "/" inside
def file(filepath): ...
```

Converters: `string` (the default), `int`, `float`, `path` and `uuid`. If the value doesn't match,
Flask responds **404** without ever reaching your function.

## The request: `flask.request`

```python
from flask import request

@app.get("/search")
def search():
    q = request.args.get("q", "")               # query string ?q=...
    page = request.args.get("page", 1, type=int)
    ...

@app.post("/products")
def create():
    data = request.get_json(silent=True)         # JSON body (None if it isn't valid JSON)
    name = request.form.get("name")              # form body
    token = request.headers.get("Authorization")
    ...
```

`request` is a **per-request global** object: Flask uses context variables (*context locals*) so
each request sees its own, even when several run in parallel. It's convenient, but "magic".
FastAPI, by contrast, passes you the data as function parameters.

`request.args.get(..., type=int)` returns the default if the conversion fails, instead of raising
an exception.

## The response

A view can return:

```python
return "text"                                   # 200, text/html
return {"id": 1, "name": "tea"}                 # a dict → JSON automatically
return jsonify([1, 2, 3])                       # explicit JSON (works for lists)
return {"error": "not found"}, 404              # (body, status)
return {"id": 7}, 201, {"Location": "/products/7"}   # (body, status, headers)
return redirect(url_for("list_products"))       # 302
abort(404)                                      # stops the view with an HTTP error
```

Status codes matter: **200** OK, **201** created, **204** no content, **400** bad request, **401**
unauthenticated, **403** forbidden, **404** not found, **422** invalid data and **500** server
error.

## Testing with `test_client`

Flask ships a client that makes requests **without starting a server**:

```python
def test_create():
    client = app.test_client()
    r = client.post("/products", json={"name": "tea", "price": 3500})
    assert r.status_code == 201
    assert r.get_json()["name"] == "tea"

    r = client.get("/search", query_string={"q": "te"})
    assert r.status_code == 200
```

`r.get_json()` parses the body and `r.text` gives it to you as a string. This is the standard way to
test Flask apps, and the one this module's tests use.

## Quick comparison of the three frameworks

| Concept           | Flask                        | FastAPI                         | Django                      |
|-------------------|------------------------------|---------------------------------|-----------------------------|
| Route             | `@app.get("/x/<int:id>")`    | `@app.get("/x/{id}")` + `id: int` | `path("x/<int:id>/", view)` |
| Request data      | global `request`             | parameters with type hints      | `request` as an argument    |
| JSON              | return a dict                | return a dict or a model        | `JsonResponse(...)`         |
| Validation        | manual or via extensions     | automatic (Pydantic)            | Forms / serializers         |
| Philosophy        | minimal, you pick the pieces | modern, typed APIs              | batteries included          |

## Summary

- `app = Flask(__name__)` and views registered with `@app.get`/`@app.post`.
- Route variables with converters (`<int:id>`); no match means 404.
- `request.args`, `request.get_json()`, `request.form` and `request.headers`.
- Returning a dict gives you JSON; `(body, status)` to pick the code; `abort()` to bail out.
- `app.test_client()` to test without a server.

## Exercise

A small in-memory products API: plain text, a route with a variable, a validated query string, a
detail view with 404 and a create endpoint with 201.

**Further reading:** [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/),
[Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/).
