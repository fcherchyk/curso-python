import itertools
import types

from ejercicio import bytes_por_status, en_lotes, parsear_accesos, primeros_cuadrados_pares

LOG = [
    "10.0.0.1 GET /index 200 512",
    "10.0.0.2 POST /api 500 128",
    "línea rota",
    "10.0.0.1 GET /img 200 2048",
    "10.0.0.3 GET /x 404 abc",
    "10.0.0.4 GET /y 404 64",
]


def test_primeros_cuadrados_pares_con_infinito():
    assert primeros_cuadrados_pares(itertools.count(1), 4) == [4, 16, 36, 64]


def test_en_lotes_con_lista():
    assert list(en_lotes([0, 1, 2, 3, 4, 5, 6], 3)) == [(0, 1, 2), (3, 4, 5), (6,)]
    assert list(en_lotes([], 3)) == []


def test_en_lotes_es_perezoso():
    lotes = en_lotes(itertools.count(), 2)
    assert next(lotes) == (0, 1)
    assert next(lotes) == (2, 3)


def test_parsear_accesos():
    res = parsear_accesos(LOG)
    assert isinstance(res, types.GeneratorType)
    assert list(res) == [
        ("10.0.0.1", 200, 512),
        ("10.0.0.2", 500, 128),
        ("10.0.0.1", 200, 2048),
        ("10.0.0.4", 404, 64),
    ]


def test_bytes_por_status():
    assert bytes_por_status(LOG) == {200: 2560, 404: 64, 500: 128}
    assert list(bytes_por_status(LOG)) == [200, 404, 500]


def test_bytes_por_status_con_generador():
    assert bytes_por_status(linea for linea in LOG) == {200: 2560, 404: 64, 500: 128}
