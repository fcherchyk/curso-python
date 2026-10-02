"""Modelos y el ORM de Django.

Los modelos ya están (este archivo hace de models.py). Escribí las consultas:

- activos_hasta(maximo) → nombres de productos ACTIVOS con precio <= maximo, del más barato
                          al más caro.
- buscar(texto)        → nombres (orden alfabético) de productos cuyo nombre O el nombre de su
                          categoría contengan `texto`, sin importar mayúsculas (Q + icontains).
- stock_por_categoria() → {nombre_categoria: stock total}, solo categorías con productos
                          (values + annotate(Sum)).
- aumentar_precios(categoria, porcentaje) → aumenta en la BASE (F + update) el precio de los
                          productos de esa categoría; devuelve cuántos actualizó.
- listado() → ["Producto (Categoría)", ...] ordenado por producto, en UNA sola consulta
              (select_related).
"""

from decimal import Decimal  # noqa: F401

from django.db import models
from django.db.models import F, Q, Sum  # noqa: F401


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
    raise NotImplementedError("TODO")


def buscar(texto: str) -> list[str]:
    raise NotImplementedError("TODO")


def stock_por_categoria() -> dict[str, int]:
    raise NotImplementedError("TODO")


def aumentar_precios(categoria: str, porcentaje: int) -> int:
    raise NotImplementedError("TODO")


def listado() -> list[str]:
    raise NotImplementedError("TODO")
