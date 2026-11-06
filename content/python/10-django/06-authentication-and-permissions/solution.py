from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import path
from django.views.decorators.http import require_http_methods


class Nota(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)

    class Meta:
        app_label = "notas"


def registrar(username: str, password: str):  # type: ignore[no-untyped-def]
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        raise ValueError("usuario existente")
    return User.objects.create_user(username, password=password)


@require_http_methods(["POST"])
def login_view(request):  # type: ignore[no-untyped-def]
    usuario = authenticate(
        request, username=request.POST.get("username"), password=request.POST.get("password")
    )
    if usuario is None:
        return JsonResponse({"error": "credenciales inválidas"}, status=400)
    login(request, usuario)
    return HttpResponse(status=204)


@require_http_methods(["POST"])
def logout_view(request):  # type: ignore[no-untyped-def]
    logout(request)
    return HttpResponse(status=204)


@login_required
@require_http_methods(["GET", "POST"])
def notas(request):  # type: ignore[no-untyped-def]
    if request.method == "POST":
        nota = Nota.objects.create(autor=request.user, texto=request.POST.get("texto", ""))
        return JsonResponse({"id": nota.id, "texto": nota.texto}, status=201)
    propias = Nota.objects.filter(autor=request.user).order_by("id")
    return JsonResponse([{"id": n.id, "texto": n.texto} for n in propias], safe=False)


@login_required
@require_http_methods(["DELETE"])
def nota(request, id: int):  # type: ignore[no-untyped-def]
    nota = get_object_or_404(Nota, id=id)
    if nota.autor != request.user and not request.user.is_staff:
        raise PermissionDenied
    nota.delete()
    return HttpResponse(status=204)


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("notas/", notas, name="notas"),
    path("notas/<int:id>/", nota, name="nota"),
]
