"""Django: URLs y vistas.

Este archivo hace de views.py + urls.py. Escribí las vistas y completá urlpatterns:

""                          name="inicio"    → HttpResponse "Hola, Django"
"saludo/<str:nombre>/"      name="saludo"    → HttpResponse "Hola, <nombre>!"
"productos/"                name="productos" → GET: lista JSON de PRODUCTOS (safe=False)
                                               POST: body JSON {"nombre", "precio"} → 201 con el
                                                     producto creado (id = máx + 1);
                                                     sin nombre o precio → 400 {"error": "datos incompletos"}
                                               otro método → 405 (require_http_methods)
"productos/<int:id>/"       name="detalle"   → JSON del producto, o 404 (raise Http404)
"""

import json  # noqa: F401

from django.http import Http404, HttpResponse, JsonResponse  # noqa: F401
from django.urls import path  # noqa: F401
from django.views.decorators.http import require_http_methods  # noqa: F401

PRODUCTOS: dict[int, dict[str, object]] = {
    1: {"id": 1, "nombre": "yerba", "precio": 3500},
    2: {"id": 2, "nombre": "café", "precio": 9800},
}

urlpatterns: list = []
