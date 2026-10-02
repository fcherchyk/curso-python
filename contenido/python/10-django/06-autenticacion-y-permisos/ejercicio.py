"""Autenticación y permisos.

El modelo Nota ya está. Escribí:

1. registrar(username, password) → User nuevo (create_user, contraseña hasheada).
   Si el username ya existe → ValueError("usuario existente").
2. Vistas:
   POST   /login/            (form username, password) → authenticate + login → 204;
                              credenciales inválidas → 400 {"error": "credenciales inválidas"}
   POST   /logout/           → logout → 204
   GET    /notas/            login_required → [{"id", "texto"}] de las notas DEL usuario
   POST   /notas/            login_required, form "texto" → 201 {"id", "texto"} con autor = usuario
   DELETE /notas/<int:id>/   login_required; 404 si no existe; solo el autor o un usuario staff
                              (si no, PermissionDenied → 403) → 204
   (GET y POST de /notas/ van en la misma vista, `notas`.)
3. URLs con name: "login", "logout", "notas", "nota".
"""

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout  # noqa: F401
from django.contrib.auth.decorators import login_required  # noqa: F401
from django.core.exceptions import PermissionDenied  # noqa: F401
from django.db import models
from django.http import HttpResponse, JsonResponse  # noqa: F401
from django.shortcuts import get_object_or_404  # noqa: F401
from django.urls import path  # noqa: F401
from django.views.decorators.http import require_http_methods  # noqa: F401


class Nota(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)

    class Meta:
        app_label = "notas"


def registrar(username: str, password: str):  # type: ignore[no-untyped-def]
    raise NotImplementedError("TODO")


urlpatterns: list = []
