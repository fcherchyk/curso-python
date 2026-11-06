"""Flask: your first app.

Add the requested routes to `app`. PRODUCTS is the in-memory "database".
"""

from flask import Flask, request  # noqa: F401

app = Flask(__name__)

PRODUCTS: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "tea", "price": 3500},
    2: {"id": 2, "name": "coffee", "price": 9800},
}

# Routes to implement:
#
# GET  /                     → text "Hello, Flask!"
# GET  /greet/<name>         → text "Hello, <name>!"
# GET  /add?a=1&b=2          → JSON {"result": 3}
#                              if a or b is missing or not an integer → 400 {"error": "a and b must be integers"}
# GET  /products/<int:id>    → the product as JSON, or 404 {"error": "product not found"}
# POST /products             → JSON body {"name": str, "price": int}
#                              creates the product with id = highest id + 1 and responds 201 with the product
#                              if name or price is missing → 400 {"error": "name and price are required"}
