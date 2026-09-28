"""Verifica TUS tests con mutation testing (ver el capítulo anterior)."""

import ast
import subprocess
import sys
import tempfile
from functools import cache
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
TUS_TESTS = (AQUI / "ejercicio.py").read_text(encoding="utf-8")
ORIGINAL = (AQUI / "clima.py").read_text(encoding="utf-8")

MUTANTES = {
    "ignora_la_ciudad_en_la_url": ("/actual?ciudad={ciudad}", "/actual"),
    "no_redondea": ('return round(datos["temp_c"], 1)', 'return datos["temp_c"]'),
    "no_omite_las_que_fallan": (
        "except LookupError:\n            continue",
        "finally:\n            pass",
    ),
    "reporte_sin_ordenar": ("sorted(temperaturas.items())", "temperaturas.items()"),
}


@cache
def correr(clima: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "clima.py").write_text(clima, encoding="utf-8")
        (d / "test_tuyos.py").write_text(TUS_TESTS, encoding="utf-8")
        (d / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=line"],
            cwd=d,
            capture_output=True,
            text=True,
            timeout=30,
        )


def test_estructura_de_tus_tests():
    arbol = ast.parse(TUS_TESTS)
    tests = [n for n in arbol.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    assert len(tests) >= 4, "escribí al menos 4 tests"
    assert "@pytest.fixture" in TUS_TESTS, "definí al menos una fixture propia"
    assert "Mock(" in TUS_TESTS, "usá unittest.mock.Mock"
    assert "tmp_path" in TUS_TESTS, "usá la fixture tmp_path"


def test_tus_tests_pasan_con_el_codigo_correcto():
    r = correr(ORIGINAL)
    assert r.returncode == 0, "tus tests fallan con el código correcto:\n" + r.stdout[-1500:]


@pytest.mark.parametrize("mutante", MUTANTES)
def test_detecta_mutante(mutante):
    assert correr(ORIGINAL).returncode == 0, "primero tus tests tienen que pasar con el original"
    buscar, reemplazo = MUTANTES[mutante]
    assert buscar in ORIGINAL
    r = correr(ORIGINAL.replace(buscar, reemplazo))
    assert r.returncode != 0, f"el mutante '{mutante}' sobrevivió: ningún test lo detectó"
