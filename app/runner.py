"""Corre los tests de un ejercicio contra el código del usuario.

El código se escribe como `ejercicio.py` en un directorio temporal junto con los tests y
se ejecuta pytest en un subproceso (con el mismo intérprete del venv) y un timeout.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

TIMEOUT_SEGUNDOS = 15
MAX_LINEAS_MENSAJE = 40


@dataclass(frozen=True)
class ResultadoTest:
    nombre: str
    ok: bool
    mensaje: str = ""


@dataclass
class ResultadoEjecucion:
    tests: list[ResultadoTest] = field(default_factory=list)
    error: str | None = None
    salida: str = ""

    @property
    def aprobado(self) -> bool:
        return self.error is None and bool(self.tests) and all(t.ok for t in self.tests)

    @property
    def cantidad_ok(self) -> int:
        return sum(t.ok for t in self.tests)


def _copiar(origen: Path, destino: Path) -> None:
    """Copia un archivo o una carpeta de soporte al directorio de trabajo."""
    if origen.is_dir():
        shutil.copytree(origen, destino / origen.name, ignore=shutil.ignore_patterns("__pycache__"))
    else:
        shutil.copy(origen, destino / origen.name)


def _recortar(texto: str, max_lineas: int = MAX_LINEAS_MENSAJE) -> str:
    lineas = texto.strip().splitlines()
    if len(lineas) > max_lineas:
        lineas = ["…", *lineas[-max_lineas:]]
    return "\n".join(lineas)


_CABECERA_FRAME = re.compile(r"^(\S.*?):(\d+|\?\?\?): in ")


def _limpiar_traza(texto: str, dir_trabajo: Path) -> str:
    """Saca rutas temporales y frames de pytest/importlib: deja solo los archivos del ejercicio."""
    for prefijo in (f"/private{dir_trabajo}/", f"{dir_trabajo}/"):
        texto = texto.replace(prefijo, "")
    lineas: list[str] = []
    saltear = False
    for linea in texto.splitlines():
        if linea.startswith("Hint:") or linea == "Traceback:":
            continue
        if _CABECERA_FRAME.match(linea) or linea.startswith("<frozen"):
            saltear = linea.startswith(("/", "<"))
        if not saltear or linea.startswith("E "):
            lineas.append(linea)
    return "\n".join(lineas)


def _parsear_junit(ruta: Path) -> ResultadoEjecucion:
    resultado = ResultadoEjecucion()
    raiz = ET.parse(ruta).getroot()
    for caso in raiz.iter("testcase"):
        problema = caso.find("failure")
        if problema is None:
            problema = caso.find("error")
        if problema is not None and problema.get("message") == "collection failure":
            texto = problema.text or "Error al importar tu código."
            resultado.error = _recortar(_limpiar_traza(texto, ruta.parent))
            continue
        if caso.find("skipped") is not None:
            continue
        mensaje = ""
        if problema is not None:
            texto = problema.text or problema.get("message", "")
            if "NotImplementedError: TODO" in texto:
                mensaje = "Pendiente: la función todavía levanta NotImplementedError."
            else:
                mensaje = _recortar(_limpiar_traza(texto, ruta.parent))
        resultado.tests.append(
            ResultadoTest(nombre=caso.get("name", "?"), ok=problema is None, mensaje=mensaje)
        )
    return resultado


def correr_tests(
    codigo: str,
    archivos: list[Path],
    timeout: float = TIMEOUT_SEGUNDOS,
) -> ResultadoEjecucion:
    """Corre pytest con `codigo` como `ejercicio.py` y los `archivos` de soporte (tests, datos)."""
    with tempfile.TemporaryDirectory(prefix="curso-") as tmp:
        dir_trabajo = Path(tmp)
        (dir_trabajo / "ejercicio.py").write_text(codigo, encoding="utf-8")
        for archivo in archivos:
            _copiar(archivo, dir_trabajo)
        # Un pytest.ini vacío fija el rootdir acá e ignora la config del proyecto.
        (dir_trabajo / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        junit = dir_trabajo / ".resultado.xml"

        comando = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--tb=short",
            "--no-header",
            "--color=no",
            "-p",
            "no:cacheprovider",
            f"--junitxml={junit}",
        ]
        entorno = {k: v for k, v in os.environ.items() if k not in {"FORCE_COLOR", "PY_COLORS"}} | {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUTF8": "1",
            "NO_COLOR": "1",
        }
        try:
            proc = subprocess.run(
                comando,
                cwd=dir_trabajo,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=entorno,
            )
        except subprocess.TimeoutExpired:
            return ResultadoEjecucion(
                error=f"Se cortó la ejecución después de {timeout:g} s. "
                "¿Hay un bucle infinito o algo que espera entrada?"
            )

        salida = _recortar(proc.stdout + proc.stderr, 80)
        if not junit.exists():
            return ResultadoEjecucion(error=salida or "pytest no generó resultados.", salida=salida)

        resultado = _parsear_junit(junit)
        resultado.salida = salida
        if not resultado.tests and resultado.error is None:
            resultado.error = "No se encontraron tests para correr."
        return resultado
