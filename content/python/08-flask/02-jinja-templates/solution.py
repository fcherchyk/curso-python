from flask import Flask, abort, render_template, render_template_string, request

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "tea", "price": 3500},
    {"id": 2, "name": "coffee", "price": 9800},
    {"id": 3, "name": "sugar", "price": 1200},
]

_SWAP_SEPARATORS = str.maketrans({",": ".", ".": ","})


@app.template_filter("money")
def money(amount: float) -> str:
    return "$ " + f"{amount:,.2f}".translate(_SWAP_SEPARATORS)


@app.get("/products")
def product_list():
    maximum = request.args.get("max", type=int)
    products = [p for p in PRODUCTS if maximum is None or p["price"] <= maximum]
    return render_template("list.html", products=sorted(products, key=lambda p: p["name"]))


@app.get("/products/<int:id>")
def product_detail(id: int):
    product = next((p for p in PRODUCTS if p["id"] == id), None)
    if product is None:
        abort(404)
    return render_template("detail.html", product=product)


@app.get("/greet/<name>")
def greet(name: str):
    # The data goes in as a variable, never concatenated into the template text.
    return render_template_string("<p>Hello, {{ name }}!</p>", name=name)
