"""Models and the Django ORM.

The models are already here (this file acts as models.py). Write the queries:

- active_up_to(max_price) → names of ACTIVE products with price <= max_price, from cheapest
                            to most expensive.
- search(text)            → names (alphabetical order) of products whose name OR the name of
                            their category contains `text`, case-insensitive (Q + icontains).
- stock_by_category()     → {category_name: total stock}, only categories with products
                            (values + annotate(Sum)).
- raise_prices(category, percent) → raises IN THE DATABASE (F + update) the price of the
                            products in that category; returns how many it updated.
- listing() → ["Product (Category)", ...] ordered by product, in ONE single query
              (select_related).
"""

from decimal import Decimal  # noqa: F401

from django.db import models
from django.db.models import F, Q, Sum  # noqa: F401


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
    raise NotImplementedError("TODO")


def search(text: str) -> list[str]:
    raise NotImplementedError("TODO")


def stock_by_category() -> dict[str, int]:
    raise NotImplementedError("TODO")


def raise_prices(category: str, percent: int) -> int:
    raise NotImplementedError("TODO")


def listing() -> list[str]:
    raise NotImplementedError("TODO")
