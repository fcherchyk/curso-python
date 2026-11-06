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
    Categoria,
    Producto,
    activos_hasta,
    aumentar_precios,
    buscar,
    listado,
    stock_por_categoria,
)


@pytest.fixture(autouse=True)
def datos():
    with connection.schema_editor() as editor:
        editor.create_model(Categoria)
        editor.create_model(Producto)
    almacen = Categoria.objects.create(nombre="Almacén")
    bebidas = Categoria.objects.create(nombre="Bebidas")
    Categoria.objects.create(nombre="Vacía")
    for nombre, precio, stock, activo, cat in [
        ("Yerba", "3500", 10, True, almacen),
        ("Azúcar", "1200", 5, True, almacen),
        ("Fideos", "900", 0, False, almacen),
        ("Agua", "800", 20, True, bebidas),
        ("Vino", "7000", 3, True, bebidas),
    ]:
        Producto.objects.create(
            nombre=nombre, precio=Decimal(precio), stock=stock, activo=activo, categoria=cat
        )
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Producto)
        editor.delete_model(Categoria)


def test_activos_hasta():
    assert activos_hasta(Decimal("3500")) == ["Agua", "Azúcar", "Yerba"]
    assert activos_hasta(Decimal("100")) == []


def test_buscar_por_nombre_o_categoria():
    assert buscar("AGU") == ["Agua"]
    assert buscar("bebi") == ["Agua", "Vino"]
    assert buscar("zúc") == ["Azúcar"]


def test_stock_por_categoria():
    assert stock_por_categoria() == {"Almacén": 15, "Bebidas": 23}


def test_aumentar_precios():
    assert aumentar_precios("Bebidas", 10) == 2
    assert Producto.objects.get(nombre="Agua").precio == Decimal("880.00")
    assert Producto.objects.get(nombre="Yerba").precio == Decimal("3500.00")


def test_aumentar_precios_en_una_consulta():
    with CaptureQueriesContext(connection) as consultas:
        aumentar_precios("Almacén", 50)
    assert len(consultas) == 1, "usá F() + update(): una sola consulta UPDATE"


def test_listado_sin_n_mas_1():
    with CaptureQueriesContext(connection) as consultas:
        res = listado()
    assert res == [
        "Agua (Bebidas)",
        "Azúcar (Almacén)",
        "Fideos (Almacén)",
        "Vino (Bebidas)",
        "Yerba (Almacén)",
    ]
    assert len(consultas) == 1, f"{len(consultas)} consultas: usá select_related"
