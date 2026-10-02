"""Corre los tests de un ejercicio contra el código del usuario.

El código se escribe como `ejercicio.py` en un directorio temporal junto con los tests y
se ejecuta pytest en un subproceso (con el mismo intérprete del venv) y un timeout.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
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
            shutil.copy(archivo, dir_trabajo / archivo.name)
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


# ---------------------------------------------------------------------------
# Go
# ---------------------------------------------------------------------------

TIMEOUT_GO_SEGUNDOS = 45  # incluye compilar; la primera vez sin build cache tarda más
GO_MOD = "module ejercicio\n\ngo 1.23\n"


_CORTE_TRAZA = re.compile(r"(?m)^(?:panic:|goroutine \d+|.*test timed out)")


def _limpiar_salida_go(lineas: list[str], dir_trabajo: Path) -> str:
    """Saca los marcos de `go test` (=== RUN, --- FAIL) y las rutas temporales."""
    utiles = []
    for linea in lineas:
        for prefijo in (f"/private{dir_trabajo}/", f"{dir_trabajo}/", "./"):
            linea = linea.replace(prefijo, "")
        if linea.lstrip().startswith(("=== ", "--- ")) or not linea.strip():
            continue
        utiles.append(linea.rstrip())
    return textwrap.dedent("\n".join(utiles)).strip()


def _parsear_go_json(salida: str, dir_trabajo: Path) -> ResultadoEjecucion:
    resultado = ResultadoEjecucion()
    salidas: dict[str, list[str]] = {}
    estados: dict[str, bool | None] = {}  # None: arrancó pero no terminó (panic)
    compilacion: list[str] = []
    salida_paquete: list[str] = []

    for linea in salida.splitlines():
        try:
            ev = json.loads(linea)
        except json.JSONDecodeError:
            compilacion.append(linea)
            continue
        accion, test = ev.get("Action"), ev.get("Test")
        if accion == "build-output":
            compilacion.append(ev.get("Output", ""))
        elif test is None:
            if accion == "output":
                salida_paquete.append(ev.get("Output", ""))
        elif accion == "run":
            estados.setdefault(test, None)
            salidas.setdefault(test, [])
        elif accion == "output":
            salidas.setdefault(test, []).append(ev.get("Output", ""))
        elif accion in ("pass", "fail"):
            estados[test] = accion == "pass"

    if compilacion and not estados:
        texto = _limpiar_salida_go("".join(compilacion).splitlines(), dir_trabajo)
        resultado.error = _recortar(texto or "No compila.")
        return resultado

    # Si un test tiene subtests, se muestran los subtests y no el padre.
    padres = {t.rsplit("/", 1)[0] for t in estados if "/" in t}
    for test, ok in estados.items():
        if test in padres:
            continue
        mensaje = ""
        if not ok:
            propias = _limpiar_salida_go(salidas.get(test, []), dir_trabajo)
            # La traza cruda (goroutines) se resume aparte en `traza`.
            propias = _CORTE_TRAZA.split(propias)[0].strip()
            # Un panic o un timeout deja la traza en el test padre o en el paquete.
            ancestros = list(salidas.get(test, []))
            partes = test.split("/")
            for i in range(len(partes) - 1, 0, -1):
                ancestros += salidas.get("/".join(partes[:i]), [])
            traza = _resumir_panic(ancestros + salida_paquete, dir_trabajo)
            mensaje = _recortar("\n\n".join(t for t in (propias, traza) if t))
        resultado.tests.append(ResultadoTest(nombre=test, ok=bool(ok), mensaje=mensaje))

    if not resultado.tests:
        texto = _limpiar_salida_go(salida_paquete, dir_trabajo)
        resultado.error = _recortar(texto or "No se encontraron tests para correr.")
    return resultado


def _resumir_panic(lineas: list[str], dir_trabajo: Path) -> str:
    """Primera línea del panic/timeout y las líneas de tu código involucradas."""
    texto = "".join(lineas)
    inicio = next(
        (i for i in (texto.find("panic:"), texto.find("test timed out")) if i >= 0), -1
    )
    if inicio < 0:
        return ""
    cabecera = texto[inicio:].split("\ngoroutine ", 1)[0].strip()
    tuyas = [
        _limpiar_salida_go([linea], dir_trabajo)
        for linea in texto[inicio:].splitlines()
        if "ejercicio.go:" in linea
    ]
    partes = [cabecera, *(f"en {t}" for t in dict.fromkeys(tuyas))]
    partes.append("(un panic o un timeout corta la ejecución del resto de los tests)")
    return "\n".join(partes)


def correr_tests_go(
    codigo: str,
    archivos: list[Path],
    timeout: float = TIMEOUT_GO_SEGUNDOS,
) -> ResultadoEjecucion:
    """Corre `go test` con `codigo` como `ejercicio.go` y los `archivos` de soporte."""
    with tempfile.TemporaryDirectory(prefix="curso-go-") as tmp:
        dir_trabajo = Path(tmp)
        (dir_trabajo / "go.mod").write_text(GO_MOD, encoding="utf-8")
        (dir_trabajo / "ejercicio.go").write_text(codigo, encoding="utf-8")
        for archivo in archivos:
            shutil.copy(archivo, dir_trabajo / archivo.name)

        entorno = os.environ | {"GOTOOLCHAIN": "local", "GOFLAGS": "-mod=mod"}
        comando = [_binario_go(), "test", "-json", "-count=1", "-timeout=10s", "./..."]
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
                error=f"Se cortó la ejecución después de {timeout:g} s. ¿Hay un bucle infinito?"
            )
        except FileNotFoundError:
            return ResultadoEjecucion(error="No se encontró el comando `go`. Instalalo con brew.")

        resultado = _parsear_go_json(proc.stdout + proc.stderr, dir_trabajo)
        resultado.salida = _recortar(proc.stderr, 80)
        return resultado


def _binario_go() -> str:
    # El servidor puede arrancar con un PATH reducido: buscamos también en Homebrew.
    return shutil.which("go") or next(
        (p for p in ("/opt/homebrew/bin/go", "/usr/local/go/bin/go") if Path(p).exists()), "go"
    )
