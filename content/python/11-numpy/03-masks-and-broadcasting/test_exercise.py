import numpy as np
from exercise import (
    centrar_columnas,
    en_rango,
    mejores,
    proporcion_sobre_promedio_por_fila,
    reemplazar_atipicos,
    tabla_de_multiplicar,
)


def test_en_rango():
    v = np.array([5, -2, 8, -1, 3, 10])
    np.testing.assert_array_equal(en_rango(v, 0, 8), [5, 8, 3])
    assert len(en_rango(v, 100, 200)) == 0


def test_reemplazar_atipicos_no_muta():
    v = np.array([1.0, -50.0, 3.0, 99.0])
    r = reemplazar_atipicos(v, 10)
    np.testing.assert_array_equal(r, [1.0, 0.0, 3.0, 0.0])
    np.testing.assert_array_equal(v, [1.0, -50.0, 3.0, 99.0])


def test_mejores():
    nombres = np.array(["ana", "beto", "caro", "dani"])
    puntajes = np.array([7, 9, 5, 8])
    assert mejores(nombres, puntajes, 2) == ["beto", "dani"]
    assert mejores(nombres, puntajes, 1) == ["beto"]


def test_centrar_columnas():
    m = np.array([[1.0, 10.0], [3.0, 20.0], [5.0, 30.0]])
    r = centrar_columnas(m)
    np.testing.assert_allclose(r, [[-2, -10], [0, 0], [2, 10]])
    np.testing.assert_allclose(r.mean(axis=0), [0, 0])


def test_proporcion_sobre_promedio_por_fila():
    m = np.array([[1, 2, 3, 10], [5, 5, 5, 5]])
    np.testing.assert_allclose(proporcion_sobre_promedio_por_fila(m), [0.25, 0.0])


def test_tabla_de_multiplicar():
    t = tabla_de_multiplicar(4)
    assert t.shape == (4, 4)
    assert t[2, 3] == 12
    np.testing.assert_array_equal(t[0], [1, 2, 3, 4])
    np.testing.assert_array_equal(t, t.T)
