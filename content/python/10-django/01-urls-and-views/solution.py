import json

from django.http import Http404, HttpResponse, JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods

PRODUCTOS: dict[int, dict[str, object]] = {
    1: {"id": 1, "nombre": "yerba", "precio": 3500},
    2: {"id": 2, "nombre": "café", "precio": 9800},
}


def inicio(request):
    return HttpResponse("Hola, Django")


def saludo(request, nombre: str):
    return HttpResponse(f"Hola, {nombre}!")


@require_http_methods(["GET", "POST"])
def productos(request):
    if request.method == "POST":
        datos = json.loads(request.body or b"{}")
        if "nombre" not in datos or "precio" not in datos:
            return JsonResponse({"error": "datos incompletos"}, status=400)
        nuevo_id = max(PRODUCTOS, default=0) + 1
        PRODUCTOS[nuevo_id] = {"id": nuevo_id, "nombre": datos["nombre"], "precio": datos["precio"]}
        return JsonResponse(PRODUCTOS[nuevo_id], status=201)
    return JsonResponse(list(PRODUCTOS.values()), safe=False)


def detalle(request, id: int):
    producto = PRODUCTOS.get(id)
    if producto is None:
        raise Http404("producto inexistente")
    return JsonResponse(producto)


urlpatterns = [
    path("", inicio, name="inicio"),
    path("saludo/<str:nombre>/", saludo, name="saludo"),
    path("productos/", productos, name="productos"),
    path("productos/<int:id>/", detalle, name="detalle"),
]
