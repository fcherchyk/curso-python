import csv
from collections import defaultdict

import pandas as pd
import pytest
from exercise import apilar, enriquecer, facturacion_por_categoria, productos_fuera_de_catalogo

with open("ventas.csv", newline="", encoding="utf-8") as f:
    VENTAS = list(csv.DictReader(f))
with open("productos.csv", newline="", encoding="utf-8") as f:
    CATALOGO = {p["producto"]: p for p in csv.DictReader(f)}


@pytest.fixture
def ventas():
    return pd.read_csv("ventas.csv")


@pytest.fixture
def productos():
    return pd.read_csv("productos.csv")


def test_enriquecer_no_pierde_filas(ventas, productos):
    r = enriquecer(ventas, productos)
    assert len(r) == len(ventas)
    assert {"categoria", "precio_unitario", "total"} <= set(r.columns)
    con_catalogo = next(v for v in VENTAS if v["producto"] in CATALOGO)
    fila = r[r["id"] == int(con_catalogo["id"])].iloc[0]
    esperado = int(con_catalogo["cantidad"]) * int(CATALOGO[con_catalogo["producto"]]["precio_unitario"])
    assert fila["total"] == esperado
    assert r.loc[r["producto"] == "mate", "categoria"].isna().all()


def test_enriquecer_valida_claves_duplicadas(ventas, productos):
    duplicado = pd.concat([productos, productos.head(1)], ignore_index=True)
    with pytest.raises(pd.errors.MergeError):
        enriquecer(ventas, duplicado)


def test_productos_fuera_de_catalogo(ventas, productos):
    esperado = sorted({v["producto"] for v in VENTAS} - set(CATALOGO))
    assert productos_fuera_de_catalogo(ventas, productos) == esperado == ["mate"]


def test_facturacion_por_categoria(ventas, productos):
    esperado: dict[str, int] = defaultdict(int)
    for v in VENTAS:
        if v["producto"] in CATALOGO:
            p = CATALOGO[v["producto"]]
            esperado[p["categoria"]] += int(v["cantidad"]) * int(p["precio_unitario"])
    r = facturacion_por_categoria(ventas, productos)
    assert r == pytest.approx(dict(esperado))


def test_apilar():
    ene = pd.DataFrame({"producto": ["a", "b"], "cantidad": [1, 2]})
    feb = pd.DataFrame({"producto": ["c"], "cantidad": [3]})
    r = apilar({"ene": ene, "feb": feb})
    assert list(r.columns) == ["lote", "producto", "cantidad"]
    assert r["lote"].tolist() == ["ene", "ene", "feb"]
    assert r.index.tolist() == [0, 1, 2]
    assert r["cantidad"].sum() == 6
