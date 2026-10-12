import matplotlib

matplotlib.use("Agg")  # sin pantalla: antes de importar pyplot

import matplotlib.pyplot as plt
import numpy as np
import pytest
from ejercicio import comparar_sucursales, grafico_ventas, guardar

MESES = ["ene", "feb", "mar", "abr"]


@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")


def test_grafico_ventas():
    fig = grafico_ventas(MESES, [10, 12, 9, 15])
    assert len(fig.axes) == 1
    assert tuple(fig.get_size_inches()) == (8, 4)
    ax = fig.axes[0]
    assert ax.get_title() == "Ventas mensuales"
    assert ax.get_xlabel() == "Mes" and ax.get_ylabel() == "Ventas ($)"
    lineas = ax.get_lines()
    assert len(lineas) == 1
    np.testing.assert_array_equal(lineas[0].get_ydata(), [10, 12, 9, 15])
    assert lineas[0].get_marker() == "o"
    assert any(linea.get_visible() for linea in ax.get_xgridlines()), "activá la grilla"


def test_comparar_sucursales():
    fig = comparar_sucursales(MESES, {"Norte": [1, 2, 3, 4], "Sur": [4, 3, 2, 1]})
    assert len(fig.axes) == 1, "las dos series van en los mismos ejes"
    ax = fig.axes[0]
    assert ax.get_title() == "Ventas por sucursal"
    assert [linea.get_label() for linea in ax.get_lines()] == ["Norte", "Sur"]
    leyenda = ax.get_legend()
    assert leyenda is not None, "falta la leyenda"
    assert [t.get_text() for t in leyenda.get_texts()] == ["Norte", "Sur"]


def test_guardar(tmp_path):
    fig = grafico_ventas(MESES, [1, 2, 3, 4])
    ruta = guardar(fig, tmp_path / "ventas.png")
    assert ruta.exists()
    assert ruta.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert not plt.fignum_exists(fig.number), "cerrá la figura después de guardar"
