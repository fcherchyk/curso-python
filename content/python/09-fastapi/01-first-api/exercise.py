"""FastAPI: your first API.

The same API as the first Flask chapter, in FastAPI:

GET  /                      → {"message": "Hello, FastAPI"}
GET  /greet/{name}          → {"greeting": "Hello, <name>!"}
GET  /add?a=1&b=2           → {"result": 3}     (a and b required and int: otherwise, automatic 422)
GET  /products              → list of products; with ?max_price=N only those with price <= N
GET  /products/{id}         → the product, or 404 with detail "product not found"
POST /products              → body NewProduct → 201 with {"id": max+1, "name", "price"}
"""

from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel

app = FastAPI(title="Store")

PRODUCTS: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "mate", "price": 3500},
    2: {"id": 2, "name": "coffee", "price": 9800},
}


class NewProduct(BaseModel):
    name: str
    price: int
