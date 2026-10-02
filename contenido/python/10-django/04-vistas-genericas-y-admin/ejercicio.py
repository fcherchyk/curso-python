"""Vistas basadas en clases y el admin.

El modelo Libro ya está. Escribí:

1. LibroLista (ListView): plantilla "libros/lista.html", variable `libros`, orden por título,
   paginate_by=3 y, si viene ?q=texto, filtrar por título (icontains).
2. LibroDetalle (DetailView): plantilla "libros/detalle.html", variable `libro`.
3. LibroCrear (CreateView): campos titulo, autor y anio; plantilla "libros/form.html";
   después de guardar redirige a la lista (reverse_lazy).
4. URLs: "libros/" name="lista", "libros/<int:pk>/" name="detalle", "libros/nuevo/" name="crear".
5. Admin: registrá Libro con list_display = ["titulo", "autor", "anio"],
   search_fields = ["titulo", "autor"] y list_filter = ["anio"].
"""

from django.contrib import admin  # noqa: F401
from django.db import models
from django.urls import path, reverse_lazy  # noqa: F401
from django.views.generic import CreateView, DetailView, ListView  # noqa: F401


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()

    class Meta:
        app_label = "biblioteca"

    def __str__(self) -> str:
        return self.titulo


urlpatterns: list = []
