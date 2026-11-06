import csv
from collections import defaultdict

import pandas as pd
import pytest
from exercise import (
    participacion_en_sucursal,
    producto_top_por_sucursal,
    resumen_por_categoria,
    tabla_sucursal_categoria,
    total_por_sucursal,
)

# Referencias calculadas en Python puro (sin pandas)
with open("ventas.csv", newline="", encoding="utf-8") as f:
    FILAS = list(csv.DictReader(f))
for fila in FILAS:
    fila["total"] = int(fila["cantidad"]) * int(fila["precio_unitario"])

POR_SUCURSAL: dict[str, int] = defaultdict(int)
for fila in FILAS:
    POR_SUCURSAL[fila["sucursal"]] += fila["total"]


@pytest.fixture
def ventas():
    df = pd.read_csv("ventas.csv", index_col="id", parse_dates=["fecha"])
    df["total"] = df["cantidad"] * df["precio_unitario"]
    return df


def test_total_por_sucursal(ventas):
    r = total_por_sucursal(ventas)
    assert r.to_dict() == dict(POR_SUCURSAL)
    assert r.is_monotonic_decreasing


def test_resumen_por_categoria(ventas):
    r = resumen_por_categoria(ventas)
    assert list(r.columns) == ["unidades", "facturacion", "ticket_promedio", "productos"]
    assert r["facturacion"].is_monotonic_decreasing
    infusiones = [f for f in FILAS if f["categoria"] == "infusiones"]
    fila = r.loc["infusiones"]
    assert fila["unidades"] == sum(int(f["cantidad"]) for f in infusiones)
    assert fila["facturacion"] == sum(f["total"] for f in infusiones)
    assert fila["ticket_promedio"] == round(sum(f["total"] for f in infusiones) / len(infusiones), 2)
    assert fila["productos"] == len({f["producto"] for f in infusiones})


def test_participacion_en_sucursal(ventas):
    r = participacion_en_sucursal(ventas)
    assert r.index.equals(ventas.index)
    primera = FILAS[0]
    assert r.loc[int(primera["id"])] == pytest.approx(primera["total"] / POR_SUCURSAL[primera["sucursal"]])
    assert r.groupby(ventas["sucursal"]).sum().round(9).eq(1).all()


def test_tabla_sucursal_categoria(ventas):
    t = tabla_sucursal_categoria(ventas)
    assert sorted(t.index) == sorted(POR_SUCURSAL)
    assert t.sum(axis=1).to_dict() == dict(POR_SUCURSAL)
    esperado = sum(f["total"] for f in FILAS if f["sucursal"] == "Sur" and f["categoria"] == "almacén")
    assert t.loc["Sur", "almacén"] == esperado
    assert (t >= 0).all().all()


def test_producto_top_por_sucursal(ventas):
    unidades: dict[tuple[str, str], int] = defaultdict(int)
    for f in FILAS:
        unidades[(f["sucursal"], f["producto"])] += int(f["cantidad"])
    esperado = {}
    for suc in POR_SUCURSAL:
        candidatos = {p: u for (s, p), u in unidades.items() if s == suc}
        esperado[suc] = max(candidatos, key=candidatos.get)
    assert producto_top_por_sucursal(ventas) == esperado
