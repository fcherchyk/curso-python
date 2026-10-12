import csv
import math
import statistics
from pathlib import Path

import pandas as pd
import pytest
from ejercicio import (
    beneficio_diversificacion,
    buy_and_hold,
    cargar,
    rebalanceo_diario,
    retorno_esperado,
    retorno_portafolio,
    retornos_simples,
    volatilidad_portafolio,
)

ACTIVOS = ["ACME", "BETA", "CIRC", "DELTA"]
PESOS = {"ACME": 0.4, "BETA": 0.3, "CIRC": 0.1, "DELTA": 0.2}

# Referencia calculada sin pandas.
with open(Path(__file__).parent / "precios.csv", encoding="utf-8") as f:
    FILAS = list(csv.DictReader(f))
P = {a: [float(f[a]) for f in FILAS] for a in ACTIVOS}
R = {a: [b / x - 1 for x, b in zip(p[:-1], p[1:], strict=True)] for a, p in P.items()}
R_PORT = [sum(PESOS[a] * R[a][t] for a in ACTIVOS) for t in range(len(FILAS) - 1)]


@pytest.fixture(scope="module")
def datos():
    precios = cargar()
    return precios, retornos_simples(precios), pd.Series(PESOS)


def test_retorno_portafolio(datos):
    _, r, w = datos
    rp = retorno_portafolio(r, w)
    assert list(rp) == pytest.approx(R_PORT)


def test_retorno_esperado(datos):
    _, r, w = datos
    assert retorno_esperado(r, w) == pytest.approx(statistics.mean(R_PORT) * 252)


def test_volatilidad_portafolio(datos):
    _, r, w = datos
    # la varianza del retorno ponderado es exactamente wᵀΣw
    assert volatilidad_portafolio(r, w) == pytest.approx(statistics.stdev(R_PORT) * math.sqrt(252))


def test_beneficio_diversificacion(datos):
    _, r, w = datos
    promedio = sum(PESOS[a] * statistics.stdev(R[a]) * math.sqrt(252) for a in ACTIVOS)
    esperado = 1 - statistics.stdev(R_PORT) * math.sqrt(252) / promedio
    assert beneficio_diversificacion(r, w) == pytest.approx(esperado)
    assert beneficio_diversificacion(r, pd.Series({"ACME": 1.0})) == pytest.approx(0, abs=1e-12)


def test_buy_and_hold(datos):
    precios, _, w = datos
    valor, pesos_finales = buy_and_hold(precios, w, 1000)
    acciones = {a: 1000 * PESOS[a] / P[a][0] for a in ACTIVOS}
    assert valor.iloc[0] == pytest.approx(1000)
    assert valor.iloc[-1] == pytest.approx(sum(acciones[a] * P[a][-1] for a in ACTIVOS))
    assert pesos_finales.sum() == pytest.approx(1)
    assert pesos_finales["ACME"] == pytest.approx(acciones["ACME"] * P["ACME"][-1] / valor.iloc[-1])


def test_rebalanceo_diario(datos):
    precios, _, w = datos
    valor = rebalanceo_diario(precios, w, 1000)
    assert len(valor) == len(FILAS) - 1
    assert valor.index[0] == pd.Timestamp(FILAS[1]["fecha"])
    assert valor.iloc[-1] == pytest.approx(1000 * math.prod(1 + x for x in R_PORT))
