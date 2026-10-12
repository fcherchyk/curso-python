import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from ejercicio import cargar, grafico_equity, posicion, resumen, retornos_estrategia, senal_cruce

# Referencia sin pandas: un backtest escrito con bucles.
with open(Path(__file__).parent / "precios.csv", encoding="utf-8") as f:
    FILAS = list(csv.DictReader(f))


def backtest_a_mano(activo, corta, larga, costo):
    p = [float(f[activo]) for f in FILAS]
    senal = []
    for t in range(len(p)):
        if t + 1 < larga:
            senal.append(0)
        else:
            mc = sum(p[t - corta + 1 : t + 1]) / corta
            ml = sum(p[t - larga + 1 : t + 1]) / larga
            senal.append(1 if mc > ml else 0)
    pos = [0] + senal[:-1]
    capital, previa, ops = 1.0, 0, 0
    for t in range(1, len(p)):
        cambio = abs(pos[t] - previa)
        ops += cambio
        capital *= 1 + pos[t] * (p[t] / p[t - 1] - 1) - costo * cambio
        previa = pos[t]
    return senal, pos, capital - 1, ops


@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")


def test_senal_cruce():
    s = senal_cruce(cargar("ACME"), 20, 50)
    senal, *_ = backtest_a_mano("ACME", 20, 50, 0)
    assert list(s) == senal
    assert s.iloc[:49].eq(0).all(), "sin datos suficientes, afuera"


def test_posicion_sin_look_ahead():
    s = pd.Series([1, 0, 1, 1], index=pd.date_range("2025-01-01", periods=4))
    pos = posicion(s)
    assert list(pos) == [0, 1, 0, 1], "la posición de hoy es la señal de ayer"


def test_retornos_estrategia():
    precios = pd.Series([100.0, 110.0, 99.0, 99.0])
    pos = pd.Series([1, 1, 0, 1])
    r = retornos_estrategia(precios, pos, costo=0.01)
    # día 0: entra (cobra costo); día 1: +10 %; día 2: sale (cobra costo); día 3: entra (cobra)
    assert list(r) == pytest.approx([-0.01, 0.10, -0.01, -0.01])


@pytest.mark.parametrize("activo", ["ACME", "INDICE"])
def test_resumen(activo):
    *_, total, ops = backtest_a_mano(activo, 20, 50, 0.001)
    res = resumen(cargar(activo))
    assert res["estrategia"] == pytest.approx(total)
    assert res["operaciones"] == ops
    p = [float(f[activo]) for f in FILAS]
    assert res["buy_and_hold"] == pytest.approx(p[-1] / p[0] - 1)
    assert 0 < res["exposicion"] < 1


def test_costos_restan():
    acme = cargar("ACME")
    assert resumen(acme, costo=0.01)["estrategia"] < resumen(acme, costo=0)["estrategia"]


def test_grafico_equity():
    fig = grafico_equity(cargar("ACME"), capital=1000)
    ax = fig.axes[0]
    assert ax.get_ylabel() == "Capital ($)"
    lineas = {ln.get_label(): ln for ln in ax.get_lines()}
    assert set(lineas) == {"Estrategia", "Buy & hold"}
    *_, total, _ = backtest_a_mano("ACME", 20, 50, 0.001)
    assert lineas["Estrategia"].get_ydata()[-1] == pytest.approx(1000 * (1 + total))
    p = [float(f["ACME"]) for f in FILAS]
    assert lineas["Buy & hold"].get_ydata()[-1] == pytest.approx(1000 * p[-1] / p[0])
    assert not math.isnan(lineas["Estrategia"].get_ydata()[0])
