"""Templates with Jinja2.

The templates live in templates/ (base.html, list.html, detail.html) and their
contents are shown in the lesson. Write:

1. The "money" template filter: 3500 → "$ 3.500,00" (dot for thousands, comma for decimals).
2. GET /products             → render "list.html" with the variable `products`
                               (the ones in PRODUCTS, sorted by name).
                               With ?max=N, only those with price <= N.
3. GET /products/<int:id>    → render "detail.html" with the variable `product`,
                               or 404 (abort) if it doesn't exist.
4. GET /greet/<name>         → render_template_string of "<p>Hello, {{ name }}!</p>"
                               (autoescaping must protect against malicious HTML).

The view function names matter: the templates use
url_for('product_list') and url_for('product_detail', id=...).
"""

from flask import Flask, abort, render_template, render_template_string, request  # noqa: F401

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "tea", "price": 3500},
    {"id": 2, "name": "coffee", "price": 9800},
    {"id": 3, "name": "sugar", "price": 1200},
]
