from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Store")

PRODUCTS: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "mate", "price": 3500},
    2: {"id": 2, "name": "coffee", "price": 9800},
}


class NewProduct(BaseModel):
    name: str
    price: int


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Hello, FastAPI"}


@app.get("/greet/{name}")
def greet(name: str) -> dict[str, str]:
    return {"greeting": f"Hello, {name}!"}


@app.get("/add")
def add(a: int, b: int) -> dict[str, int]:
    return {"result": a + b}


@app.get("/products")
def list_products(max_price: int | None = None) -> list[dict[str, object]]:
    return [
        p for p in PRODUCTS.values() if max_price is None or int(p["price"]) <= max_price
    ]


@app.get("/products/{id}")
def detail(id: int) -> dict[str, object]:
    product = PRODUCTS.get(id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@app.post("/products", status_code=201)
def create(data: NewProduct) -> dict[str, object]:
    new_id = max(PRODUCTS, default=0) + 1
    product = {"id": new_id, **data.model_dump()}
    PRODUCTS[new_id] = product
    return product
