from flask import Flask, request

app = Flask(__name__)

PRODUCTS: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "tea", "price": 3500},
    2: {"id": 2, "name": "coffee", "price": 9800},
}


@app.get("/")
def index():
    return "Hello, Flask!"


@app.get("/greet/<name>")
def greet(name: str):
    return f"Hello, {name}!"


@app.get("/add")
def add():
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    if a is None or b is None:
        return {"error": "a and b must be integers"}, 400
    return {"result": a + b}


@app.get("/products/<int:id>")
def detail(id: int):
    product = PRODUCTS.get(id)
    if product is None:
        return {"error": "product not found"}, 404
    return product


@app.post("/products")
def create():
    data = request.get_json(silent=True) or {}
    if "name" not in data or "price" not in data:
        return {"error": "name and price are required"}, 400
    new_id = max(PRODUCTS, default=0) + 1
    product = {"id": new_id, "name": data["name"], "price": data["price"]}
    PRODUCTS[new_id] = product
    return product, 201
