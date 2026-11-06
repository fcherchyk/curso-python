"""Django REST Framework.

The Task model is already here. Write:

1. TaskSerializer (ModelSerializer): fields id, title, done, created; id and created are read-only.
   validate_title: no surrounding spaces; "todo" (ignoring case/spaces) is not allowed →
   ValidationError("Use a descriptive title").
2. TaskViewSet (ModelViewSet): queryset ordered by id; with ?done=true|false it filters.
   @action complete (POST /api/tasks/{pk}/complete/) → marks it done and returns the task.
3. Stats (APIView): GET /api/stats/ → {"total", "done", "pending"}.
4. URLs: a DefaultRouter with "tasks" under "api/", and "api/stats/".
"""

from django.db import models
from django.urls import include, path  # noqa: F401
from rest_framework import serializers, viewsets  # noqa: F401
from rest_framework.decorators import action  # noqa: F401
from rest_framework.response import Response  # noqa: F401
from rest_framework.routers import DefaultRouter  # noqa: F401
from rest_framework.views import APIView  # noqa: F401


class Task(models.Model):
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "tasks"


urlpatterns: list = []
