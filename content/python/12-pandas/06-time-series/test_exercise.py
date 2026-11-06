import csv
from datetime import date

import pandas as pd
import pytest
from exercise import (
    cargar_precios,
    cierres_mensuales,
    cruces_alcistas,
    rendimiento_por_anio,
    retornos_mensuales,
)

# Referencia en Python puro: fecha → precio de ACME
with open("precios.csv", newline="", encoding="utf-8") as f:
    ACME = [(date.fromisoformat(r["fecha"]), float(r["ACME"])) for r in csv.DictReader(f)]


def ultimo_de(anio: int, mes: int | None = None) -> float:
    return [p for d, p in ACME if d.year == anio and (mes is None or d.month == mes)][-1]


@pytest.fixture(scope="module")
def precios():
    return cargar_precios("precios.csv")


def test_cargar_precios(precios):
    assert isinstance(precios.index, pd.DatetimeIndex)
    assert precios.index.name == "fecha"
    assert list(precios.columns) == ["ACME", "BETA", "CIRC", "DELTA", "INDICE"]


def test_cierres_mensuales(precios):
    m = cierres_mensuales(precios)
    assert len(m) == 36
    assert m.loc["2024-03", "ACME"].iloc[0] == ultimo_de(2024, 3)


def test_retornos_mensuales(precios):
    r = retornos_mensuales(precios)
    assert len(r) == 35
    assert not r.isna().any().any()
    esperado = ultimo_de(2024, 3) / ultimo_de(2024, 2) - 1
    assert r.loc["2024-03", "ACME"].iloc[0] == pytest.approx(esperado)


def test_rendimiento_por_anio(precios):
    r = rendimiento_por_anio(precios, "ACME")
    assert set(r) == {2023, 2024, 2025}
    assert r[2023] == round(ultimo_de(2023) / ACME[0][1] - 1, 4)
    assert r[2025] == round(ultimo_de(2025) / ultimo_de(2024) - 1, 4)


def test_cruces_alcistas(precios):
    cruces = cruces_alcistas(precios["ACME"], 20, 50)
    assert cruces, "tiene que haber al menos un cruce"
    fechas = [d for d, _ in ACME]
    valores = [p for _, p in ACME]

    def media(fin: int, n: int) -> float:
        return sum(valores[fin - n + 1 : fin + 1]) / n

    for c in cruces:
        i = fechas.index(c.date())
        assert i >= 50, "no puede haber cruces antes de tener 50 datos"
        assert media(i, 20) > media(i, 50)
        assert media(i - 1, 20) <= media(i - 1, 50)
