from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import path
from django.views.decorators.http import require_http_methods


class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    class Meta:
        app_label = "notes"


def register(username: str, password: str):  # type: ignore[no-untyped-def]
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        raise ValueError("user already exists")
    return User.objects.create_user(username, password=password)


@require_http_methods(["POST"])
def login_view(request):  # type: ignore[no-untyped-def]
    user = authenticate(
        request, username=request.POST.get("username"), password=request.POST.get("password")
    )
    if user is None:
        return JsonResponse({"error": "invalid credentials"}, status=400)
    login(request, user)
    return HttpResponse(status=204)


@require_http_methods(["POST"])
def logout_view(request):  # type: ignore[no-untyped-def]
    logout(request)
    return HttpResponse(status=204)


@login_required
@require_http_methods(["GET", "POST"])
def notes(request):  # type: ignore[no-untyped-def]
    if request.method == "POST":
        note = Note.objects.create(author=request.user, text=request.POST.get("text", ""))
        return JsonResponse({"id": note.id, "text": note.text}, status=201)
    own = Note.objects.filter(author=request.user).order_by("id")
    return JsonResponse([{"id": n.id, "text": n.text} for n in own], safe=False)


@login_required
@require_http_methods(["DELETE"])
def note(request, id: int):  # type: ignore[no-untyped-def]
    note = get_object_or_404(Note, id=id)
    if note.author != request.user and not request.user.is_staff:
        raise PermissionDenied
    note.delete()
    return HttpResponse(status=204)


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("notes/", notes, name="notes"),
    path("notes/<int:id>/", note, name="note"),
]
