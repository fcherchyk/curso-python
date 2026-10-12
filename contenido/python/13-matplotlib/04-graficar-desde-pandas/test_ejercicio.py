import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from ejercicio import barras_por_categoria, cargar, estilizar, lineas_por_sucursal


@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")


def totales(clave):
    """Referencia calculada sin pandas, con el módulo csv."""
    acum = defaultdict(int)
    with open(Path(__file__).parent / "ventas.csv", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            acum[clave(fila)] += int(fila["cantidad"]) * int(fila["precio_unitario"])
    return acum


def test_estilizar():
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    devuelto = estilizar(ax, "T", "X", "Y")
    assert devuelto is ax
    assert (ax.get_title(), ax.get_xlabel(), ax.get_ylabel()) == ("T", "X", "Y")
    assert not ax.spines["top"].get_visible() and not ax.spines["right"].get_visible()
    assert ax.spines["left"].get_visible() and ax.spines["bottom"].get_visible()
    assert any(g.get_visible() for g in ax.yaxis.get_gridlines()), "grilla en Y"
    assert not any(g.get_visible() for g in ax.xaxis.get_gridlines()), "sin grilla en X"


def test_lineas_por_sucursal():
    fig = lineas_por_sucursal(cargar())
    ax = fig.axes[0]
    assert ax.get_title() == "Importe mensual por sucursal"
    assert ax.get_ylabel() == "Importe ($)"
    assert not ax.spines["top"].get_visible(), "aplicá estilizar"
    ref = totales(lambda f: (f["sucursal"], f["fecha"][:7]))
    leyenda = [t.get_text() for t in ax.get_legend().get_texts()]
    assert sorted(leyenda) == ["Centro", "Norte", "Sur"]
    for linea, sucursal in zip(ax.get_lines(), leyenda, strict=True):
        assert linea.get_marker() == "o"
        esperado = [ref[(sucursal, m)] for m in ("2025-01", "2025-02", "2025-03")]
        assert list(linea.get_ydata()) == esperado, sucursal


def test_barras_por_categoria():
    fig = barras_por_categoria(cargar())
    ax = fig.axes[0]
    assert ax.get_title() == "Importe por categoría"
    assert ax.get_xlabel() == "Importe ($)" and ax.get_ylabel() == ""
    assert not ax.spines["right"].get_visible(), "aplicá estilizar"
    ref = totales(lambda f: f["categoria"])
    esperado = sorted(ref.items(), key=lambda kv: kv[1])
    assert [t.get_text() for t in ax.get_yticklabels()] == [k for k, _ in esperado]
    assert [b.get_width() for b in ax.patches] == [v for _, v in esperado]
