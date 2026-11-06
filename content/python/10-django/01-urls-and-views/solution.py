import json

from django.http import Http404, HttpResponse, JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods

PRODUCTS: dict[int, dict[str, object]] = {
    1: {"id": 1, "name": "mate", "price": 3500},
    2: {"id": 2, "name": "coffee", "price": 9800},
}


def home(request):
    return HttpResponse("Hello, Django")


def greet(request, name: str):
    return HttpResponse(f"Hello, {name}!")


@require_http_methods(["GET", "POST"])
def products(request):
    if request.method == "POST":
        data = json.loads(request.body or b"{}")
        if "name" not in data or "price" not in data:
            return JsonResponse({"error": "incomplete data"}, status=400)
        new_id = max(PRODUCTS, default=0) + 1
        PRODUCTS[new_id] = {"id": new_id, "name": data["name"], "price": data["price"]}
        return JsonResponse(PRODUCTS[new_id], status=201)
    return JsonResponse(list(PRODUCTS.values()), safe=False)


def detail(request, id: int):
    product = PRODUCTS.get(id)
    if product is None:
        raise Http404("product not found")
    return JsonResponse(product)


urlpatterns = [
    path("", home, name="home"),
    path("greet/<str:name>/", greet, name="greet"),
    path("products/", products, name="products"),
    path("products/<int:id>/", detail, name="detail"),
]
