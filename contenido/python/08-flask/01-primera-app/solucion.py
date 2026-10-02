from flask import Flask, request

app = Flask(__name__)

PRODUCTOS: dict[int, dict[str, object]] = {
    1: {"id": 1, "nombre": "yerba", "precio": 3500},
    2: {"id": 2, "nombre": "café", "precio": 9800},
}


@app.get("/")
def inicio():
    return "Hola, Flask!"


@app.get("/saludo/<nombre>")
def saludo(nombre: str):
    return f"Hola, {nombre}!"


@app.get("/sumar")
def sumar():
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    if a is None or b is None:
        return {"error": "a y b tienen que ser enteros"}, 400
    return {"resultado": a + b}


@app.get("/productos/<int:id>")
def detalle(id: int):
    producto = PRODUCTOS.get(id)
    if producto is None:
        return {"error": "producto inexistente"}, 404
    return producto


@app.post("/productos")
def crear():
    datos = request.get_json(silent=True) or {}
    if "nombre" not in datos or "precio" not in datos:
        return {"error": "nombre y precio son obligatorios"}, 400
    nuevo_id = max(PRODUCTOS, default=0) + 1
    producto = {"id": nuevo_id, "nombre": datos["nombre"], "precio": datos["precio"]}
    PRODUCTOS[nuevo_id] = producto
    return producto, 201
