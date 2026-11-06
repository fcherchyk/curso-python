from decimal import Decimal

from django.db import models
from django.db.models import F, Q, Sum


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = "catalog"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")

    class Meta:
        app_label = "catalog"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


def active_up_to(max_price: Decimal) -> list[str]:
    qs = Product.objects.filter(active=True, price__lte=max_price).order_by("price")
    return list(qs.values_list("name", flat=True))


def search(text: str) -> list[str]:
    qs = Product.objects.filter(
        Q(name__icontains=text) | Q(category__name__icontains=text)
    ).order_by("name")
    return list(qs.values_list("name", flat=True))


def stock_by_category() -> dict[str, int]:
    rows = Product.objects.values("category__name").annotate(total=Sum("stock"))
    return {r["category__name"]: r["total"] for r in rows}


def raise_prices(category: str, percent: int) -> int:
    factor = Decimal(100 + percent) / 100
    return Product.objects.filter(category__name=category).update(price=F("price") * factor)


def listing() -> list[str]:
    return [f"{p.name} ({p.category.name})" for p in Product.objects.select_related("category")]
