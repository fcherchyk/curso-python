"""FastAPI: tu primera API.

La misma API del primer capítulo de Flask, en FastAPI:

GET  /                      → {"mensaje": "Hola, FastAPI"}
GET  /saludo/{nombre}       → {"saludo": "Hola, <nombre>!"}
GET  /sumar?a=1&b=2         → {"resultado": 3}     (a y b obligatorios e int: si no, 422 automático)
GET  /productos             → lista de productos; con ?max_precio=N solo los de precio <= N
GET  /productos/{id}        → el producto, o 404 con detail "producto inexistente"
POST /productos             → body ProductoNuevo → 201 con {"id": máx+1, "nombre", "precio"}
"""

from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel

app = FastAPI(title="Tienda")

PRODUCTOS: dict[int, dict[str, object]] = {
    1: {"id": 1, "nombre": "yerba", "precio": 3500},
    2: {"id": 2, "nombre": "café", "precio": 9800},
}


class ProductoNuevo(BaseModel):
    nombre: str
    precio: int
