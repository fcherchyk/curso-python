import csv
import math
import statistics
from pathlib import Path

import pytest
from exercise import beta, cargar, menos_correlacionado, retornos_simples, sharpe, sortino

# Referencia calculada sin pandas.
with open(Path(__file__).parent / "precios.csv", encoding="utf-8") as f:
    FILAS = list(csv.DictReader(f))


def rets(col):
    p = [float(f[col]) for f in FILAS]
    return [b / a - 1 for a, b in zip(p[:-1], p[1:], strict=True)]


ACME, INDICE = rets("ACME"), rets("INDICE")
EXCESO = [x - 0.04 / 252 for x in ACME]


@pytest.fixture(scope="module")
def r():
    return retornos_simples(cargar())


def test_sharpe(r):
    s = sharpe(r)
    esperado = statistics.mean(EXCESO) / statistics.stdev(ACME) * math.sqrt(252)
    assert s["ACME"] == pytest.approx(esperado)
    assert s.idxmax() == "DELTA"
    assert sharpe(r, tasa_libre=0)["ACME"] > s["ACME"]


def test_sortino(r):
    abajo = math.sqrt(statistics.mean(min(x, 0) ** 2 for x in EXCESO)) * math.sqrt(252)
    esperado = statistics.mean(EXCESO) * 252 / abajo
    assert sortino(r)["ACME"] == pytest.approx(esperado)


def test_beta(r):
    b = beta(r)
    assert "INDICE" not in b.index
    esperado = statistics.covariance(ACME, INDICE) / statistics.variance(INDICE)
    assert b["ACME"] == pytest.approx(esperado)
    assert b.idxmax() == "CIRC" and b.idxmin() == "DELTA"


def test_menos_correlacionado(r):
    assert menos_correlacionado(r, "ACME") == "DELTA"
    candidatos = ["ACME", "BETA", "DELTA", "INDICE"]
    esperado = min(candidatos, key=lambda c: statistics.correlation(rets("CIRC"), rets(c)))
    assert menos_correlacionado(r, "CIRC") == esperado
