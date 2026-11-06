import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
)
django.setup()

from decimal import Decimal

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from exercise import (
    Category,
    Product,
    active_up_to,
    listing,
    raise_prices,
    search,
    stock_by_category,
)


@pytest.fixture(autouse=True)
def data():
    with connection.schema_editor() as editor:
        editor.create_model(Category)
        editor.create_model(Product)
    pantry = Category.objects.create(name="Pantry")
    drinks = Category.objects.create(name="Drinks")
    Category.objects.create(name="Empty")
    for name, price, stock, active, cat in [
        ("Mate", "3500", 10, True, pantry),
        ("Sugar", "1200", 5, True, pantry),
        ("Pasta", "900", 0, False, pantry),
        ("Water", "800", 20, True, drinks),
        ("Wine", "7000", 3, True, drinks),
    ]:
        Product.objects.create(
            name=name, price=Decimal(price), stock=stock, active=active, category=cat
        )
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Product)
        editor.delete_model(Category)


def test_active_up_to():
    assert active_up_to(Decimal("3500")) == ["Water", "Sugar", "Mate"]
    assert active_up_to(Decimal("100")) == []


def test_search_by_name_or_category():
    assert search("WAT") == ["Water"]
    assert search("drin") == ["Water", "Wine"]
    assert search("uga") == ["Sugar"]


def test_stock_by_category():
    assert stock_by_category() == {"Pantry": 15, "Drinks": 23}


def test_raise_prices():
    assert raise_prices("Drinks", 10) == 2
    assert Product.objects.get(name="Water").price == Decimal("880.00")
    assert Product.objects.get(name="Mate").price == Decimal("3500.00")


def test_raise_prices_in_one_query():
    with CaptureQueriesContext(connection) as queries:
        raise_prices("Pantry", 50)
    assert len(queries) == 1, "use F() + update(): a single UPDATE query"


def test_listing_without_n_plus_1():
    with CaptureQueriesContext(connection) as queries:
        res = listing()
    assert res == [
        "Mate (Pantry)",
        "Pasta (Pantry)",
        "Sugar (Pantry)",
        "Water (Drinks)",
        "Wine (Drinks)",
    ]
    assert len(queries) == 1, f"{len(queries)} queries: use select_related"
