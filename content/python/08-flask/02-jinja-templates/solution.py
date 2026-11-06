from flask import Flask, abort, render_template, render_template_string, request

app = Flask(__name__)

PRODUCTOS = [
    {"id": 1, "nombre": "yerba", "precio": 3500},
    {"id": 2, "nombre": "café", "precio": 9800},
    {"id": 3, "nombre": "azúcar", "precio": 1200},
]

_A_FORMATO_AR = str.maketrans({",": ".", ".": ","})


@app.template_filter("pesos")
def pesos(monto: float) -> str:
    return "$ " + f"{monto:,.2f}".translate(_A_FORMATO_AR)


@app.get("/productos")
def lista():
    maximo = request.args.get("max", type=int)
    productos = [p for p in PRODUCTOS if maximo is None or p["precio"] <= maximo]
    return render_template("lista.html", productos=sorted(productos, key=lambda p: p["nombre"]))


@app.get("/productos/<int:id>")
def detalle(id: int):
    producto = next((p for p in PRODUCTOS if p["id"] == id), None)
    if producto is None:
        abort(404)
    return render_template("detalle.html", producto=producto)


@app.get("/saludo/<nombre>")
def saludo(nombre: str):
    # El dato va como variable, nunca concatenado en el texto de la plantilla.
    return render_template_string("<p>Hola, {{ nombre }}!</p>", nombre=nombre)
