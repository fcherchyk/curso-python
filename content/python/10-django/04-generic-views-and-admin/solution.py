from django.contrib import admin
from django.db import models
from django.urls import path, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()

    class Meta:
        app_label = "biblioteca"

    def __str__(self) -> str:
        return self.titulo


class LibroLista(ListView):
    model = Libro
    ordering = ["titulo"]
    paginate_by = 3
    template_name = "libros/lista.html"
    context_object_name = "libros"

    def get_queryset(self):  # type: ignore[no-untyped-def]
        qs = super().get_queryset()
        if q := self.request.GET.get("q"):
            qs = qs.filter(titulo__icontains=q)
        return qs


class LibroDetalle(DetailView):
    model = Libro
    template_name = "libros/detalle.html"
    context_object_name = "libro"


class LibroCrear(CreateView):
    model = Libro
    fields = ["titulo", "autor", "anio"]
    template_name = "libros/form.html"
    success_url = reverse_lazy("lista")


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ["titulo", "autor", "anio"]
    search_fields = ["titulo", "autor"]
    list_filter = ["anio"]


urlpatterns = [
    path("libros/", LibroLista.as_view(), name="lista"),
    path("libros/<int:pk>/", LibroDetalle.as_view(), name="detalle"),
    path("libros/nuevo/", LibroCrear.as_view(), name="crear"),
]
