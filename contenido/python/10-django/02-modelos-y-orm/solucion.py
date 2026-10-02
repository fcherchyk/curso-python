from decimal import Decimal

from django.db import models
from django.db.models import F, Q, Sum


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = "catalogo"

    def __str__(self) -> str:
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")

    class Meta:
        app_label = "catalogo"
        ordering = ["nombre"]

    def __str__(self) -> str:
        return self.nombre


def activos_hasta(maximo: Decimal) -> list[str]:
    qs = Producto.objects.filter(activo=True, precio__lte=maximo).order_by("precio")
    return list(qs.values_list("nombre", flat=True))


def buscar(texto: str) -> list[str]:
    qs = Producto.objects.filter(
        Q(nombre__icontains=texto) | Q(categoria__nombre__icontains=texto)
    ).order_by("nombre")
    return list(qs.values_list("nombre", flat=True))


def stock_por_categoria() -> dict[str, int]:
    filas = Producto.objects.values("categoria__nombre").annotate(total=Sum("stock"))
    return {f["categoria__nombre"]: f["total"] for f in filas}


def aumentar_precios(categoria: str, porcentaje: int) -> int:
    factor = Decimal(100 + porcentaje) / 100
    return Producto.objects.filter(categoria__nombre=categoria).update(precio=F("precio") * factor)


def listado() -> list[str]:
    return [f"{p.nombre} ({p.categoria.nombre})" for p in Producto.objects.select_related("categoria")]
