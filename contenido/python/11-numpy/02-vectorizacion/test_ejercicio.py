import time

import numpy as np
import pytest
from ejercicio import normalizar, precios_finales, suma_de_cuadrados, total_factura, variaciones


def test_total_factura():
    precios = np.array([100.0, 250.0, 80.0])
    cantidades = np.array([2, 1, 5])
    assert total_factura(precios, cantidades) == pytest.approx(1028.5)
    assert total_factura(precios, cantidades, iva=0) == pytest.approx(850.0)


def test_normalizar():
    np.testing.assert_allclose(normalizar(np.array([10, 20, 30])), [0, 0.5, 1])
    r = normalizar(np.array([5, 5, 5]))
    np.testing.assert_array_equal(r, [0.0, 0.0, 0.0])
    assert r.dtype == np.float64


def test_precios_finales():
    r = precios_finales(np.array([100.0, 300.0, 2000.0, -5.0]), umbral=200)
    np.testing.assert_allclose(r, [100.0, 270.0, 1000.0, 0.0])


def test_variaciones():
    np.testing.assert_allclose(variaciones(np.array([100, 110, 99])), [0.1, -0.1])
    assert len(variaciones(np.arange(1, 11))) == 9


def test_suma_de_cuadrados_correcta():
    assert suma_de_cuadrados(np.array([1.0, 2.0, 3.0])) == pytest.approx(14.0)


def test_suma_de_cuadrados_es_vectorizada():
    v = np.random.default_rng(0).random(500_000)
    inicio = time.perf_counter()
    lenta = sum(x * x for x in v)
    t_bucle = time.perf_counter() - inicio

    inicio = time.perf_counter()
    rapida = suma_de_cuadrados(v)
    t_numpy = time.perf_counter() - inicio

    assert rapida == pytest.approx(lenta)
    assert t_numpy < t_bucle / 5, f"numpy {t_numpy:.4f}s vs bucle {t_bucle:.4f}s: ¿usaste un for?"
