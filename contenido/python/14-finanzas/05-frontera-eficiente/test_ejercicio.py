import csv
import math
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest
from ejercicio import (
    cargar,
    grafico_frontera,
    max_sharpe,
    min_varianza,
    pesos_aleatorios,
    retornos_simples,
    simular,
)

ACTIVOS = ["ACME", "BETA", "CIRC", "DELTA"]

# Referencia sin pandas.
with open(Path(__file__).parent / "precios.csv", encoding="utf-8") as f:
    FILAS = list(csv.DictReader(f))
P = {a: [float(f[a]) for f in FILAS] for a in ACTIVOS}
R = {a: [b / x - 1 for x, b in zip(p[:-1], p[1:], strict=True)] for a, p in P.items()}


def ref(pesos):
    """Retorno y volatilidad anual de un portafolio, sumando a mano."""
    rp = [sum(w * R[a][t] for a, w in zip(ACTIVOS, pesos, strict=True)) for t in range(len(FILAS) - 1)]
    return statistics.mean(rp) * 252, statistics.stdev(rp) * math.sqrt(252)


@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")


@pytest.fixture(scope="module")
def sim():
    return simular(retornos_simples(cargar()), 2000, semilla=7)


def test_pesos_aleatorios():
    w = pesos_aleatorios(100, 4, semilla=1)
    assert w.shape == (100, 4)
    np.testing.assert_allclose(w.sum(axis=1), 1)
    assert (w >= 0).all()
    crudo = np.random.default_rng(1).random((100, 4))
    np.testing.assert_allclose(w, crudo / crudo.sum(axis=1, keepdims=True))
    assert not np.allclose(w, pesos_aleatorios(100, 4, semilla=2))


def test_simular(sim):
    assert len(sim) == 2000
    assert set(ACTIVOS + ["retorno", "volatilidad", "sharpe"]) <= set(sim.columns)
    for i in (0, 1234):
        fila = sim.iloc[i]
        ret, vol = ref([fila[a] for a in ACTIVOS])
        assert fila["retorno"] == pytest.approx(ret)
        assert fila["volatilidad"] == pytest.approx(vol)
        assert fila["sharpe"] == pytest.approx((ret - 0.04) / vol)


def test_max_sharpe_y_min_varianza(sim):
    mejor = max_sharpe(sim)
    menos_riesgo = min_varianza(sim)
    assert mejor["sharpe"] == pytest.approx(sim["sharpe"].max())
    assert menos_riesgo["volatilidad"] == pytest.approx(sim["volatilidad"].min())
    assert mejor["DELTA"] > 0.5, "DELTA domina: baja vol, buen retorno y poca correlación"


def test_grafico_frontera(sim):
    fig = grafico_frontera(sim)
    ax = fig.axes[0]
    assert (ax.get_xlabel(), ax.get_ylabel()) == ("Volatilidad anual", "Retorno anual")
    nube, *destacados = ax.collections
    assert len(nube.get_offsets()) == 2000
    np.testing.assert_allclose(nube.get_array(), sim["sharpe"])
    leyenda = {t.get_text() for t in ax.get_legend().get_texts()}
    assert leyenda == {"Máximo Sharpe", "Mínima varianza"}
    puntos = {tuple(np.round(c.get_offsets()[0], 10)) for c in destacados}
    mejor = max_sharpe(sim)
    assert (round(mejor["volatilidad"], 10), round(mejor["retorno"], 10)) in puntos
