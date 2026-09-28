from pathlib import Path

import pytest

from app.runner import correr_tests

TESTS = """\
from ejercicio import doble


def test_doble():
    assert doble(2) == 4


def test_doble_negativo():
    assert doble(-3) == -6
"""


@pytest.fixture
def archivos(tmp_path: Path) -> list[Path]:
    ruta = tmp_path / "test_ejercicio.py"
    ruta.write_text(TESTS)
    return [ruta]


def test_codigo_correcto(archivos):
    r = correr_tests("def doble(x):\n    return x * 2\n", archivos)
    assert r.aprobado
    assert r.cantidad_ok == 2
    assert [t.nombre for t in r.tests] == ["test_doble", "test_doble_negativo"]


def test_codigo_incorrecto_muestra_el_assert(archivos):
    r = correr_tests("def doble(x):\n    return x + 2\n", archivos)
    assert not r.aprobado
    assert r.cantidad_ok == 1
    fallido = next(t for t in r.tests if not t.ok)
    assert "assert" in fallido.mensaje
    assert "/tmp" not in fallido.mensaje and "curso-" not in fallido.mensaje


def test_todo_pendiente(archivos):
    r = correr_tests('def doble(x):\n    raise NotImplementedError("TODO")\n', archivos)
    assert r.cantidad_ok == 0
    assert all("Pendiente" in t.mensaje for t in r.tests)


def test_error_de_sintaxis(archivos):
    r = correr_tests("def doble(x:\n", archivos)
    assert not r.aprobado
    assert r.error is not None and "SyntaxError" in r.error
    assert "site-packages" not in r.error


def test_bucle_infinito_corta_por_timeout(archivos):
    r = correr_tests("while True:\n    pass\n", archivos, timeout=2)
    assert not r.aprobado
    assert r.error is not None and "Se cortó" in r.error
