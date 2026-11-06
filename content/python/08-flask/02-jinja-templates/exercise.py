"""Plantillas con Jinja2.

Las plantillas están en templates/ (base.html, lista.html, detalle.html) y su
contenido está en la lección. Escribí:

1. El filtro de plantilla "pesos": 3500 → "$ 3.500,00" (punto de miles, coma decimal).
2. GET /productos            → render de "lista.html" con la variable `productos`
                               (los de PRODUCTOS ordenados por nombre).
                               Con ?max=N, solo los de precio <= N.
3. GET /productos/<int:id>   → render de "detalle.html" con la variable `producto`,
                               o 404 (abort) si no existe.
4. GET /saludo/<nombre>      → render_template_string de "<p>Hola, {{ nombre }}!</p>"
                               (el autoescape tiene que proteger del HTML malicioso).

Los nombres de las funciones de las vistas importan: las plantillas usan
url_for('lista') y url_for('detalle', id=...).
"""

from flask import Flask, abort, render_template, render_template_string, request  # noqa: F401

app = Flask(__name__)

PRODUCTOS = [
    {"id": 1, "nombre": "yerba", "precio": 3500},
    {"id": 2, "nombre": "café", "precio": 9800},
    {"id": 3, "nombre": "azúcar", "precio": 1200},
]
