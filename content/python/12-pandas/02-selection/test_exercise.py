import csv

import pandas as pd
import pytest
from exercise import (
    con_descuento,
    consulta,
    de_productos,
    top_y_primera_etiqueta,
    ventas_grandes_de,
)

with open("ventas.csv", newline="", encoding="utf-8") as f:
    FILAS = [
        {**f_, "id": int(f_["id"]), "cantidad": int(f_["cantidad"]), "precio": int(f_["precio_unitario"])}
        for f_ in csv.DictReader(f)
    ]
for f_ in FILAS:
    f_["total"] = f_["cantidad"] * f_["precio"]


@pytest.fixture
def ventas():
    df = pd.read_csv("ventas.csv", index_col="id", parse_dates=["fecha"])
    df["total"] = df["cantidad"] * df["precio_unitario"]
    return df


def test_ventas_grandes_de(ventas):
    r = ventas_grandes_de(ventas, "Centro", 10_000)
    esperado = sorted(
        (f for f in FILAS if f["sucursal"] == "Centro" and f["total"] >= 10_000),
        key=lambda f: -f["total"],
    )
    assert list(r.columns) == ["producto", "total"]
    assert r["total"].tolist() == [f["total"] for f in esperado]


def test_de_productos(ventas):
    r = de_productos(ventas, ["yerba", "mate"])
    assert r.sum() == sum(f["cantidad"] for f in FILAS if f["producto"] in ("yerba", "mate"))


def test_consulta(ventas):
    esperado = sorted(f["id"] for f in FILAS if f["categoria"] == "infusiones" and f["cantidad"] >= 5)
    assert consulta(ventas, "infusiones", 5) == esperado


def test_top_y_primera_etiqueta(ventas):
    top = max(FILAS, key=lambda f: f["total"])
    assert top_y_primera_etiqueta(ventas) == (top["id"], FILAS[0]["cantidad"])


def test_con_descuento_no_muta(ventas):
    antes = ventas.copy()
    r = con_descuento(ventas, "infusiones", 0.1)
    pd.testing.assert_frame_equal(ventas, antes)
    infusion = next(f for f in FILAS if f["categoria"] == "infusiones")
    otra = next(f for f in FILAS if f["categoria"] != "infusiones")
    assert r.loc[infusion["id"], "precio_unitario"] == pytest.approx(infusion["precio"] * 0.9)
    assert r.loc[infusion["id"], "total"] == pytest.approx(infusion["total"] * 0.9)
    assert r.loc[otra["id"], "total"] == otra["total"]
