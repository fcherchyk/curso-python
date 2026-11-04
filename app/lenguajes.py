"""Lo que cambia entre lenguajes: nombres de archivo, editor, resaltado y runner."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from app.runner import ResultadoEjecucion, correr_tests


@dataclass(frozen=True)
class Lenguaje:
    nombre: str
    archivo_ejercicio: str
    archivo_tests: str
    archivo_solucion: str
    modo_editor: str  # modo de CodeMirror 5
    lexer: str  # lexer de Pygments
    indentar_con_tabs: bool
    donde_estan_las_consignas: str
    correr: Callable[[str, list[Path]], ResultadoEjecucion]

    @property
    def archivos_privados(self) -> frozenset[str]:
        """Archivos del capítulo que NO se copian al directorio donde corren los tests."""
        return frozenset(
            {"leccion.md", "quiz.toml", self.archivo_ejercicio, self.archivo_solucion}
        )


PYTHON = Lenguaje(
    nombre="python",
    archivo_ejercicio="ejercicio.py",
    archivo_tests="test_ejercicio.py",
    archivo_solucion="solucion.py",
    modo_editor="python",
    lexer="python",
    indentar_con_tabs=False,
    donde_estan_las_consignas="los docstrings",
    correr=correr_tests,
)

LENGUAJES = {lenguaje.nombre: lenguaje for lenguaje in (PYTHON,)}
