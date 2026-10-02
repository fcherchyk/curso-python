import subprocess
import sys
from pathlib import Path

import pytest
from ejercicio import buscar_usuario, normalizar_tags, promedio_ponderado

ARCHIVO = Path(__file__).parent / "ejercicio.py"


def correr(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", *args, str(ARCHIVO)],
        capture_output=True,
        text=True,
        cwd=ARCHIVO.parent,
    )


def test_promedio_ponderado():
    assert promedio_ponderado([10, 20], [1, 3]) == 17.5
    with pytest.raises(ValueError):
        promedio_ponderado([1, 2], [1])
    with pytest.raises(ValueError):
        promedio_ponderado([1], [0])


def test_normalizar_tags():
    assert normalizar_tags([" Python", "python ", "", "  ", "Web", "API"]) == [
        "api",
        "python",
        "web",
    ]


def test_buscar_usuario():
    usuarios = {1: "ana", 2: "beto"}
    assert buscar_usuario(usuarios, 2) == "BETO"
    assert buscar_usuario(usuarios, 9) is None


def test_ruff_limpio():
    r = correr("ruff", "check", "--isolated", "--select", "E,F,I,UP,B,SIM", "--line-length", "100")
    assert r.returncode == 0, "ruff encontró problemas:\n" + r.stdout


def test_mypy_strict():
    r = correr("mypy", "--strict", "--no-incremental", "--cache-dir", "/dev/null")
    assert r.returncode == 0, "mypy encontró problemas:\n" + r.stdout
