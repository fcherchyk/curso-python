import csv
from collections import Counter

import pandas as pd
import pytest
from exercise import cargar_ventas, desde_registros, resumen, serie_precios

with open("ventas.csv", newline="", encoding="utf-8") as f:
    FILAS = list(csv.DictReader(f))  # referencia calculada sin pandas


def test_serie_precios():
    s = serie_precios({"té": 1200, "café": 9800, "azúcar": 900})
    assert isinstance(s, pd.Series)
    assert s.name == "precio"
    assert list(s.index) == ["azúcar", "café", "té"]
    assert s["café"] == 9800


def test_desde_registros():
    df = desde_registros([{"stock": 3, "producto": "yerba", "precio": 3500}])
    assert list(df.columns) == ["producto", "precio", "stock"]
    assert df.loc[0, "producto"] == "yerba"


def test_cargar_ventas_tipos():
    df = cargar_ventas("ventas.csv")
    assert df.index.name == "id"
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])
    assert len(df) == len(FILAS)
    fila = FILAS[0]
    assert df.loc[int(fila["id"]), "total"] == int(fila["cantidad"]) * int(fila["precio_unitario"])


def test_resumen():
    totales = {int(f["id"]): int(f["cantidad"]) * int(f["precio_unitario"]) for f in FILAS}
    r = resumen(cargar_ventas("ventas.csv"))
    assert r["filas"] == len(FILAS)
    assert r["total"] == sum(totales.values())
    assert r["ticket_promedio"] == pytest.approx(round(sum(totales.values()) / len(FILAS), 2))
    assert r["venta_mayor"] == max(totales, key=totales.get)
    assert r["sucursal_mas_frecuente"] == Counter(f["sucursal"] for f in FILAS).most_common(1)[0][0]
