import csv
import math
from datetime import date
from pathlib import Path

import pytest
from exercise import (
    cagr,
    cargar,
    retorno_acumulado,
    retorno_anualizado,
    retornos_log,
    retornos_simples,
)

# Referencia calculada sin pandas, con el módulo csv.
with open(Path(__file__).parent / "precios.csv", encoding="utf-8") as f:
    FILAS = list(csv.DictReader(f))
ACME = [float(f["ACME"]) for f in FILAS]


def test_retornos_simples():
    r = retornos_simples(cargar())
    assert len(r) == len(FILAS) - 1, "sacá la primera fila con dropna()"
    assert not r.isna().any().any()
    assert r["ACME"].iloc[0] == pytest.approx(ACME[1] / ACME[0] - 1)
    assert r["ACME"].iloc[-1] == pytest.approx(ACME[-1] / ACME[-2] - 1)


def test_retornos_log():
    r = retornos_log(cargar())
    assert len(r) == len(FILAS) - 1
    assert r["ACME"].iloc[0] == pytest.approx(math.log(ACME[1] / ACME[0]))
    assert r["ACME"].sum() == pytest.approx(math.log(ACME[-1] / ACME[0])), "los log se suman"


def test_retorno_acumulado():
    acum = retorno_acumulado(retornos_simples(cargar()))
    assert acum["ACME"] == pytest.approx(ACME[-1] / ACME[0] - 1)
    assert acum["BETA"] < 0


def test_retorno_anualizado():
    anual = retorno_anualizado(retornos_simples(cargar()))
    n = len(ACME) - 1
    assert anual["ACME"] == pytest.approx((ACME[-1] / ACME[0]) ** (252 / n) - 1)


def test_cagr():
    c = cagr(cargar())
    anios = (date.fromisoformat(FILAS[-1]["fecha"]) - date.fromisoformat(FILAS[0]["fecha"])).days / 365.25
    assert c["ACME"] == pytest.approx((ACME[-1] / ACME[0]) ** (1 / anios) - 1)
    assert set(c.index) == {"ACME", "BETA", "CIRC", "DELTA", "INDICE"}
