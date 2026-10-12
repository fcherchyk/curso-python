import numpy as np
import pytest
from ejercicio import (
    intervalo_bootstrap,
    mejor_dia_por_producto,
    prob_suma_dados,
    resumen_por_columna,
)


def test_resumen_por_columna():
    m = np.array([[1.0, 10.0], [3.0, np.nan], [5.0, 30.0]])
    r = resumen_por_columna(m)
    np.testing.assert_allclose(r["media"], [3.0, 20.0])
    np.testing.assert_allclose(r["desvio"], [2.0, np.std([10, 30], ddof=1)])
    np.testing.assert_allclose(r["minimo"], [1.0, 10.0])
    np.testing.assert_allclose(r["maximo"], [5.0, 30.0])


def test_mejor_dia_por_producto():
    ventas = np.array([[5, 2, 0, 7], [3, 8, 1, 2], [6, 1, 4, 9]])
    dias = np.array(["lun", "mar", "mié"])
    assert mejor_dia_por_producto(ventas, dias) == ["mié", "mar", "mié", "mié"]


def test_prob_suma_dados():
    p = prob_suma_dados(7, 200_000, semilla=1)
    assert p == pytest.approx(1 / 6, abs=0.01)
    assert prob_suma_dados(12, 200_000, semilla=1) == pytest.approx(1 / 36, abs=0.005)
    assert prob_suma_dados(13, 1000, semilla=1) == 0.0


def test_prob_suma_dados_reproducible():
    assert prob_suma_dados(7, 1000, semilla=5) == prob_suma_dados(7, 1000, semilla=5)


def test_intervalo_bootstrap():
    muestra = np.random.default_rng(0).normal(loc=50, scale=10, size=200)
    bajo, alto = intervalo_bootstrap(muestra, 5000, semilla=3)
    assert bajo < muestra.mean() < alto
    assert 2 < alto - bajo < 4  # ≈ 2 * 1.96 * 10 / sqrt(200) ≈ 2.8
    assert intervalo_bootstrap(muestra, 500, semilla=9) == intervalo_bootstrap(muestra, 500, semilla=9)
