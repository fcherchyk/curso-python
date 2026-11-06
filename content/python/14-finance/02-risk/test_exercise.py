import csv
import math
import statistics
from pathlib import Path

import numpy as np
import pytest
from exercise import (
    cargar,
    cvar_historico,
    drawdown,
    max_drawdown,
    retornos_simples,
    var_historico,
    volatilidad_anual,
)

# Referencia calculada sin pandas.
with open(Path(__file__).parent / "precios.csv", encoding="utf-8") as f:
    CIRC = [float(fila["CIRC"]) for fila in csv.DictReader(f)]
R = [b / a - 1 for a, b in zip(CIRC[:-1], CIRC[1:], strict=True)]


def test_volatilidad_anual():
    vol = volatilidad_anual(retornos_simples(cargar()))
    assert vol["CIRC"] == pytest.approx(statistics.stdev(R) * math.sqrt(252))
    assert vol.idxmin() == "DELTA"


def test_drawdown():
    dd = drawdown(cargar())
    pico, esperado = CIRC[0], []
    for p in CIRC:
        pico = max(pico, p)
        esperado.append(p / pico - 1)
    np.testing.assert_allclose(dd["CIRC"].to_numpy(), esperado)
    assert (dd <= 0).all().all()


def test_max_drawdown():
    mdd = max_drawdown(cargar())
    pico, peor = CIRC[0], 0.0
    for p in CIRC:
        pico = max(pico, p)
        peor = min(peor, p / pico - 1)
    assert mdd["CIRC"] == pytest.approx(peor)
    assert mdd.idxmin() == "CIRC"


def test_var_historico():
    r = retornos_simples(cargar())
    var = var_historico(r)
    assert var["CIRC"] == pytest.approx(-np.quantile(R, 0.05))
    assert var["CIRC"] > 0, "expresalo como pérdida positiva"
    assert var_historico(r, 0.99)["CIRC"] > var["CIRC"]


def test_cvar_historico():
    r = retornos_simples(cargar())
    corte = np.quantile(R, 0.05)
    cola = [x for x in R if x <= corte]
    cvar = cvar_historico(r)
    assert cvar["CIRC"] == pytest.approx(-statistics.mean(cola))
    assert (cvar >= var_historico(r)).all()
