"""Verifica TUS tests con mutation testing: tienen que pasar con el código correcto y
fallar con cada mutante (una versión de calendario.py con un bug introducido)."""

import ast
import subprocess
import sys
import tempfile
from functools import cache
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
TUS_TESTS = (AQUI / "ejercicio.py").read_text(encoding="utf-8")
ORIGINAL = (AQUI / "calendario.py").read_text(encoding="utf-8")

MUTANTES = {
    "bisiesto_sin_regla_del_100": (
        "anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)",
        "anio % 4 == 0",
    ),
    "bisiesto_sin_regla_del_400": (
        "anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)",
        "anio % 4 == 0 and anio % 100 != 0",
    ),
    "no_valida_el_mes": ("if not 1 <= mes <= 12:", "if not 1 <= mes <= 13:"),
    "febrero_siempre_28": ("return 29 if es_bisiesto(anio) else 28", "return 28"),
    "noviembre_con_31": ("mes in (4, 6, 9, 11)", "mes in (4, 6, 9)"),
}


@cache
def correr(calendario: str) -> subprocess.CompletedProcess[str]:
    """Corre tus tests con la versión dada de calendario.py."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "calendario.py").write_text(calendario, encoding="utf-8")
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
    nombres = [n.name for n in arbol.body if isinstance(n, ast.FunctionDef)]
    assert len([n for n in nombres if n.startswith("test_")]) >= 4, "escribí al menos 4 tests"
    assert "parametrize" in TUS_TESTS, "usá @pytest.mark.parametrize"
    assert "pytest.raises" in TUS_TESTS, "usá pytest.raises"


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
