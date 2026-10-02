import shutil
from pathlib import Path

import pytest

from app.runner import correr_tests, correr_tests_go

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


# --- Go ---------------------------------------------------------------------

TESTS_GO = """package ejercicio

import "testing"

func TestDoble(t *testing.T) {
	casos := []struct {
		nombre   string
		in, want int
	}{{"positivo", 2, 4}, {"cero", 0, 0}, {"negativo", -3, -6}}
	for _, c := range casos {
		t.Run(c.nombre, func(t *testing.T) {
			if got := Doble(c.in); got != c.want {
				t.Errorf("Doble(%d) = %d, quiero %d", c.in, got, c.want)
			}
		})
	}
}
"""

requiere_go = pytest.mark.skipif(shutil.which("go") is None, reason="go no está instalado")


def go(cuerpo: str) -> str:
    return f"package ejercicio\n\nfunc Doble(x int) int {{ {cuerpo} }}\n"


@pytest.fixture
def archivos_go(tmp_path: Path) -> list[Path]:
    ruta = tmp_path / "ejercicio_test.go"
    ruta.write_text(TESTS_GO)
    return [ruta]


@requiere_go
def test_go_correcto_muestra_subtests(archivos_go):
    r = correr_tests_go(go("return x * 2"), archivos_go)
    assert r.aprobado
    nombres = [t.nombre for t in r.tests]
    assert nombres == ["TestDoble/positivo", "TestDoble/cero", "TestDoble/negativo"]


@requiere_go
def test_go_incorrecto_muestra_el_error(archivos_go):
    r = correr_tests_go(go("return 0"), archivos_go)
    assert not r.aprobado
    fallido = next(t for t in r.tests if not t.ok)
    assert "Doble(2) = 0, quiero 4" in fallido.mensaje
    assert "=== RUN" not in fallido.mensaje


@requiere_go
def test_go_error_de_compilacion(archivos_go):
    r = correr_tests_go(go("return y"), archivos_go)
    assert r.error is not None and "undefined: y" in r.error
    assert "curso-go-" not in r.error


@requiere_go
def test_go_panic_resume_la_traza(archivos_go):
    r = correr_tests_go(go("var s []int; return s[x]"), archivos_go)
    fallido = next(t for t in r.tests if not t.ok)
    assert "index out of range" in fallido.mensaje
    assert "ejercicio.go:3" in fallido.mensaje
    assert "goroutine" not in fallido.mensaje
