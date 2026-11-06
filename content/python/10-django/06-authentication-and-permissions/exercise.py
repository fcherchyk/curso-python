"""Authentication and permissions.

The Note model is already here. Write:

1. register(username, password) → new User (create_user, hashed password).
   If the username already exists → ValueError("user already exists").
2. Views:
   POST   /login/            (form username, password) → authenticate + login → 204;
                              invalid credentials → 400 {"error": "invalid credentials"}
   POST   /logout/           → logout → 204
   GET    /notes/            login_required → [{"id", "text"}] of the user's OWN notes
   POST   /notes/            login_required, form "text" → 201 {"id", "text"} with author = user
   DELETE /notes/<int:id>/   login_required; 404 if it doesn't exist; only the author or a staff
                              user (otherwise PermissionDenied → 403) → 204
   (GET and POST on /notes/ go in the same view, `notes`.)
3. URLs with name: "login", "logout", "notes", "note".
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


class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    class Meta:
        app_label = "notes"


def register(username: str, password: str):  # type: ignore[no-untyped-def]
    raise NotImplementedError("TODO")


urlpatterns: list = []
