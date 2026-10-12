import numpy as np
from ejercicio import bordes, normalizar_copia, poner_en_cero_el_medio, puntos, tablero


def test_tablero():
    t = tablero(2, 3)
    assert t.shape == (2, 3)
    assert t.dtype == np.int64
    np.testing.assert_array_equal(t, [[1, 2, 3], [4, 5, 6]])
    assert tablero(3, 1).tolist() == [[1], [2], [3]]


def test_puntos():
    p = puntos(0, 1, 5)
    assert p.dtype == np.float64
    np.testing.assert_allclose(p, [0, 0.25, 0.5, 0.75, 1])
    assert len(puntos(-1, 1, 11)) == 11


def test_bordes():
    m = np.arange(1, 10).reshape(3, 3)
    col, fila, diag = bordes(m)
    np.testing.assert_array_equal(col, [1, 4, 7])
    np.testing.assert_array_equal(fila, [7, 8, 9])
    np.testing.assert_array_equal(diag, [1, 5, 9])


def test_normalizar_copia_no_modifica():
    base = np.array([1, 2, 4, 8])
    vista = base[1:]
    r = normalizar_copia(vista)
    np.testing.assert_allclose(r, [0.25, 0.5, 1.0])
    assert r.dtype == np.float64
    np.testing.assert_array_equal(base, [1, 2, 4, 8])


def test_poner_en_cero_el_medio_en_el_lugar():
    base = np.arange(10)
    vista = base[2:8]  # [2 3 4 5 6 7]
    assert poner_en_cero_el_medio(vista) is None
    np.testing.assert_array_equal(vista, [2, 0, 0, 0, 0, 7])
    np.testing.assert_array_equal(base, [0, 1, 2, 0, 0, 0, 0, 7, 8, 9])  # la vista comparte datos
