import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest
from ejercicio import barras_ordenadas, dispersion, histograma, tipo_recomendado


@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")


def test_barras_ordenadas():
    fig = barras_ordenadas({"Norte": 245, "Sur": 380, "Centro": 230}, "Facturación")
    ax = fig.axes[0]
    assert ax.get_title() == "Facturación"
    barras = ax.patches
    assert len(barras) == 3
    anchos = [b.get_width() for b in barras]  # en barh, el valor es el ancho
    assert anchos == [230, 245, 380], "de menor a mayor, para que la mayor quede arriba"
    etiquetas = [t.get_text() for t in ax.get_yticklabels()]
    assert etiquetas == ["Centro", "Norte", "Sur"]
    assert len(ax.texts) == 3, "agregá los valores con bar_label"


def test_dispersion():
    fig = dispersion([1, 2, 3], [2, 4, 7], "Publicidad", "Ventas")
    ax = fig.axes[0]
    puntos = ax.collections[0]
    np.testing.assert_array_equal(puntos.get_offsets(), [[1, 2], [2, 4], [3, 7]])
    assert puntos.get_alpha() == pytest.approx(0.6)
    assert (ax.get_xlabel(), ax.get_ylabel()) == ("Publicidad", "Ventas")


def test_histograma():
    valores = np.random.default_rng(0).normal(10, 2, 500)
    fig = histograma(valores, 25)
    ax = fig.axes[0]
    assert len(ax.patches) == 25
    assert sum(b.get_height() for b in ax.patches) == 500
    lineas = ax.get_lines()
    assert len(lineas) == 1 and lineas[0].get_linestyle() == "--"
    assert lineas[0].get_xdata()[0] == pytest.approx(valores.mean())
    assert ax.get_legend() is not None


def test_tipo_recomendado():
    assert tipo_recomendado("evolucion") == "linea"
    assert tipo_recomendado("comparacion") == "barras"
    assert tipo_recomendado("relacion") == "dispersion"
    assert tipo_recomendado("distribucion") == "histograma"
    with pytest.raises(ValueError):
        tipo_recomendado("proporcion de pizza")
