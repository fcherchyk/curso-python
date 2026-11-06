"""Django REST Framework.

El modelo Tarea ya está. Escribí:

1. TareaSerializer (ModelSerializer): campos id, titulo, hecha, creada; id y creada de solo lectura.
   validate_titulo: sin espacios alrededor; "todo" (sin importar mayúsculas/espacios) no vale →
   ValidationError("Poné un título descriptivo").
2. TareaViewSet (ModelViewSet): queryset ordenado por id; con ?hecha=true|false filtra.
   @action completar (POST /api/tareas/{pk}/completar/) → marca hecha y devuelve la tarea.
3. Estadisticas (APIView): GET /api/estadisticas/ → {"total", "hechas", "pendientes"}.
4. URLs: router DefaultRouter con "tareas" bajo "api/", y "api/estadisticas/".
"""

from django.db import models
from django.urls import include, path  # noqa: F401
from rest_framework import serializers, viewsets  # noqa: F401
from rest_framework.decorators import action  # noqa: F401
from rest_framework.response import Response  # noqa: F401
from rest_framework.routers import DefaultRouter  # noqa: F401
from rest_framework.views import APIView  # noqa: F401


class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    hecha = models.BooleanField(default=False)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "tareas"


urlpatterns: list = []
