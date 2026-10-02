import subprocess
import sys
import types
from datetime import datetime
from pathlib import Path

import pytest
from ejercicio import (
    LineaInvalida,
    Metodo,
    Registro,
    Resumen,
    formatear,
    main,
    parsear,
    parsear_linea,
    resumir,
    top_rutas,
)

AQUI = Path(__file__).parent

LOG = """\
2026-09-20T10:00:00 GET /api/users 200 100ms
2026-09-20T10:00:01 GET /api/users 200 120ms
2026-09-20T10:00:02 POST /api/orders 201 300ms
2026-09-20T10:00:03 GET /api/report 500 900ms

2026-09-20T10:00:04 GET /api/users 404 80ms
linea rota
2026-09-20T10:00:05 DELETE /api/orders 204 150ms
"""


@pytest.fixture
def registros():
    return list(parsear(LOG.splitlines(keepends=True)))


# --- parseo ---------------------------------------------------------------


def test_parsear_linea():
    r = parsear_linea("2026-09-20T10:15:32 GET /api/users 200 123ms\n")
    assert r == Registro(datetime(2026, 9, 20, 10, 15, 32), Metodo.GET, "/api/users", 200, 123)
    assert not r.es_error
    assert parsear_linea("2026-09-20T10:15:32 POST /x 503 1ms").es_error


@pytest.mark.parametrize(
    "linea",
    [
        "cualquier cosa",
        "2026-09-20T10:15:32 GET /api 200",  # falta duración
        "2026-09-20T10:15:32 FOO /api 200 5ms",  # método desconocido
        "2026-13-45T10:15:32 GET /api 200 5ms",  # fecha imposible
    ],
)
def test_parsear_linea_invalida(linea):
    with pytest.raises(LineaInvalida, match="api|cualquier"):
        parsear_linea(linea)


def test_linea_invalida_encadena_la_causa():
    with pytest.raises(LineaInvalida) as info:
        parsear_linea("2026-13-45T10:15:32 GET /api 200 5ms")
    assert isinstance(info.value.__cause__, ValueError), "usá `raise ... from e`"


def test_parsear_es_generador_y_junta_invalidas():
    invalidas = []
    gen = parsear(LOG.splitlines(keepends=True), invalidas)
    assert isinstance(gen, types.GeneratorType)
    regs = list(gen)
    assert len(regs) == 6
    assert invalidas == ["linea rota"]


def test_parsear_sin_lista_de_invalidas():
    assert len(list(parsear(["basura", ""]))) == 0


# --- análisis -------------------------------------------------------------


def test_resumir(registros):
    r = resumir(registros)
    assert r.total == 6
    assert r.errores == 1
    assert r.tasa_error == pytest.approx(1 / 6)
    assert r.por_status == {200: 2, 201: 1, 204: 1, 404: 1, 500: 1}
    assert list(r.por_status) == [200, 201, 204, 404, 500]
    assert r.p50_ms == 135.0
    assert r.p95_ms == 750.0
    assert r.ruta_mas_lenta == "/api/report"


def test_resumir_acepta_generador():
    assert resumir(parsear(LOG.splitlines())).total == 6


def test_resumir_casos_borde():
    vacio = resumir([])
    assert vacio == Resumen(0, 0, {}, 0.0, 0.0, "")
    assert vacio.tasa_error == 0.0
    uno = resumir([parsear_linea("2026-09-20T10:00:00 GET /a 200 42ms")])
    assert (uno.p50_ms, uno.p95_ms) == (42.0, 42.0)


def test_top_rutas(registros):
    assert top_rutas(registros, 2) == [("/api/users", 3), ("/api/orders", 2)]
    assert len(top_rutas(registros)) == 3


# --- salida y CLI ---------------------------------------------------------

REPORTE = """\
Requests: 6 (inválidas: 1)
Errores 5xx: 1 (16.7%)
Latencia p50: 135.0 ms | p95: 750.0 ms
Ruta más lenta: /api/report
Status:
  200: 2
  201: 1
  204: 1
  404: 1
  500: 1
Top rutas:
  /api/users        3
  /api/orders       2"""


def test_formatear(registros):
    assert formatear(resumir(registros), top_rutas(registros, 2), 1) == REPORTE


def test_main(tmp_path, capsys):
    log = tmp_path / "access.log"
    log.write_text(LOG, encoding="utf-8")
    assert main([str(log), "--top", "2"]) == 0
    assert capsys.readouterr().out == REPORTE + "\n"


def test_main_archivo_inexistente(tmp_path, capsys):
    assert main([str(tmp_path / "nada.log")]) == 1
    assert "No existe" in capsys.readouterr().err


def test_cli_de_verdad_sobre_access_log():
    r = subprocess.run(
        [sys.executable, "ejercicio.py", "access.log", "--top", "3"],
        cwd=AQUI,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("Requests: ")
    assert r.stdout.count("\n  /") == 3, "tiene que listar 3 rutas en el top"
