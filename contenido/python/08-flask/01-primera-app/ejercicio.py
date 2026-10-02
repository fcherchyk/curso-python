"""Flask: tu primera app.

Agregá las rutas pedidas a `app`. PRODUCTOS es la "base de datos" en memoria.
"""

from flask import Flask, request  # noqa: F401

app = Flask(__name__)

PRODUCTOS: dict[int, dict[str, object]] = {
    1: {"id": 1, "nombre": "yerba", "precio": 3500},
    2: {"id": 2, "nombre": "café", "precio": 9800},
}

# Rutas a implementar:
#
# GET  /                     → texto "Hola, Flask!"
# GET  /saludo/<nombre>      → texto "Hola, <nombre>!"
# GET  /sumar?a=1&b=2        → JSON {"resultado": 3}
#                              si falta a o b, o no son enteros → 400 {"error": "a y b tienen que ser enteros"}
# GET  /productos/<int:id>   → JSON del producto, o 404 {"error": "producto inexistente"}
# POST /productos            → body JSON {"nombre": str, "precio": int}
#                              crea el producto con id = máximo id + 1 y responde 201 con el producto
#                              si falta nombre o precio → 400 {"error": "nombre y precio son obligatorios"}
