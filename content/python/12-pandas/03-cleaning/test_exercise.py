import math

import pandas as pd
import pytest
from exercise import convertir_montos, limpiar_clientes, normalizar_nombres, nulos_por_columna


@pytest.fixture
def crudo():
    return pd.read_csv("clientes.csv", dtype=str, keep_default_na=False, na_values=[""])


def test_normalizar_nombres():
    s = pd.Series(["  ana   PÉREZ ", "beto", None])
    r = normalizar_nombres(s)
    assert r.iloc[0] == "Ana Pérez"
    assert r.iloc[1] == "Beto"
    assert pd.isna(r.iloc[2])


def test_convertir_montos():
    r = convertir_montos(pd.Series(["$ 1.234,50", "$ 20.000,75", "$ 0,00", None, "abc"]))
    assert r.iloc[0] == pytest.approx(1234.5)
    assert r.iloc[1] == pytest.approx(20000.75)
    assert r.iloc[2] == 0
    assert math.isnan(r.iloc[3]) and math.isnan(r.iloc[4])


def test_nulos_por_columna(crudo):
    assert nulos_por_columna(crudo) == {"nombre": 1, "email": 1, "saldo": 1, "ciudad": 1}


def test_limpiar_clientes(crudo):
    antes = crudo.copy()
    df = limpiar_clientes(crudo)
    pd.testing.assert_frame_equal(crudo, antes)  # no muta la entrada

    assert df["email"].tolist() == [
        "ana@mail.com",
        "beto@mail.com",
        "caro@mail.com",
        "dani@mail.com",
        "x@mail.com",
    ]
    assert df.index.tolist() == [0, 1, 2, 3, 4]
    assert df.loc[0, "nombre"] == "Ana Pérez"
    assert df.loc[1, "nombre"] == "Beto Gómez"
    assert str(df["edad"].dtype) == "Int64"
    assert pd.isna(df.loc[2, "edad"]) and df.loc[0, "edad"] == 31
    assert df.loc[0, "saldo"] == pytest.approx(1234.5)
    assert math.isnan(df.loc[2, "saldo"])
    assert df["ciudad"].tolist() == ["Rosario", "Rosario", "Córdoba", "Desconocida", "Salta"]
