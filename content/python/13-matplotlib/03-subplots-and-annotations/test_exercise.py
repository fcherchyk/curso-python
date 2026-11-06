import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from exercise import crecimiento_log, marcar_maximo, paneles


@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")


MESES = ["ene", "feb", "mar"]
SERIES = {"Norte": [10, 12, 9], "Sur": [100, 120, 130], "Centro": [50, 40, 60]}


def test_paneles():
    fig = paneles(MESES, SERIES)
    assert len(fig.axes) == 3
    assert fig.get_suptitle() == "Ventas por sucursal"
    for ax, (nombre, valores) in zip(fig.axes, SERIES.items(), strict=True):
        assert ax.get_title() == nombre
        assert list(ax.get_lines()[0].get_ydata()) == valores
    # en una fila: todos los paneles a la misma altura
    assert len({round(ax.get_position().y0, 3) for ax in fig.axes}) == 1
    # con sharey, los tres paneles tienen el mismo rango vertical
    assert len({ax.get_ylim() for ax in fig.axes}) == 1, "usá sharey=True"


def test_crecimiento_log():
    fig = crecimiento_log([2020, 2021, 2022], [100, 1000, 10000])
    ax = fig.axes[0]
    assert ax.get_yscale() == "log"
    assert ax.get_ylabel() == "Valor (escala log)"
    assert list(ax.get_lines()[0].get_ydata()) == [100, 1000, 10000]


def test_marcar_maximo():
    x, y = [1, 2, 3, 4], [5, 9, 7, 3]
    fig = marcar_maximo(x, y)
    ax = fig.axes[0]
    anotaciones = [t for t in ax.texts if isinstance(t, matplotlib.text.Annotation)]
    assert len(anotaciones) == 1, "usá ax.annotate"
    nota = anotaciones[0]
    assert nota.get_text() == "máximo"
    assert tuple(nota.xy) == (2, 9)
    assert nota.arrow_patch is not None, "agregá la flecha con arrowprops"
    horizontales = [ln for ln in ax.get_lines() if list(ln.get_xdata()) == [0, 1]]
    assert len(horizontales) == 1, "agregá ax.axhline en la media"
    assert horizontales[0].get_ydata()[0] == pytest.approx(6)
