from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Tienda")

PRODUCTOS: dict[int, dict[str, object]] = {
    1: {"id": 1, "nombre": "yerba", "precio": 3500},
    2: {"id": 2, "nombre": "café", "precio": 9800},
}


class ProductoNuevo(BaseModel):
    nombre: str
    precio: int


@app.get("/")
def inicio() -> dict[str, str]:
    return {"mensaje": "Hola, FastAPI"}


@app.get("/saludo/{nombre}")
def saludo(nombre: str) -> dict[str, str]:
    return {"saludo": f"Hola, {nombre}!"}


@app.get("/sumar")
def sumar(a: int, b: int) -> dict[str, int]:
    return {"resultado": a + b}


@app.get("/productos")
def listar(max_precio: int | None = None) -> list[dict[str, object]]:
    return [
        p for p in PRODUCTOS.values() if max_precio is None or int(p["precio"]) <= max_precio
    ]


@app.get("/productos/{id}")
def detalle(id: int) -> dict[str, object]:
    producto = PRODUCTOS.get(id)
    if producto is None:
        raise HTTPException(status_code=404, detail="producto inexistente")
    return producto


@app.post("/productos", status_code=201)
def crear(datos: ProductoNuevo) -> dict[str, object]:
    nuevo_id = max(PRODUCTOS, default=0) + 1
    producto = {"id": nuevo_id, **datos.model_dump()}
    PRODUCTOS[nuevo_id] = producto
    return producto
