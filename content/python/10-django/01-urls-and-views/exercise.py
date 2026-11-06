"""Django: URLs and views.

This file acts as views.py + urls.py. Write the views and fill in urlpatterns:

""                          name="home"      → HttpResponse "Hello, Django"
"greet/<str:name>/"         name="greet"     → HttpResponse "Hello, <name>!"
"products/"                 name="products"  → GET: JSON list of PRODUCTS (safe=False)
                                               POST: JSON body {"name", "price"} → 201 with the
                                                     created product (id = max + 1);
                                                     missing name or price → 400 {"error": "incomplete data"}
                                               any other method → 405 (require_http_methods)
"products/<int:id>/"        name="detail"    → the product as JSON, or 404 (raise Http404)
"""

import json  # noqa: F401

from django.http import Http404, HttpResponse, JsonResponse  # noqa: F401
from django.urls import path  # noqa: F401
from django.views.decorators.http import require_http_methods  # noqa: F401

PRODUCTS: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "mate", "price": 3500},
    2: {"id": 2, "name": "coffee", "price": 9800},
}

urlpatterns: list = []
