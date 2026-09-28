from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.contenido import cargar_temario
from app.main import crear_app

CAP = cargar_temario().capitulos()[0]
URL = f"/c/{CAP.id}"


@pytest.fixture
def cliente(tmp_path: Path) -> TestClient:
    return TestClient(crear_app(ruta_db=tmp_path / "progreso.db"))


def respuestas_correctas() -> dict[str, str]:
    return {f"p{i}": str(p.correcta) for i, p in enumerate(CAP.preguntas())}


def test_indice(cliente):
    r = cliente.get("/")
    assert r.status_code == 200
    assert CAP.titulo in r.text


def test_capitulo(cliente):
    r = cliente.get(URL)
    assert r.status_code == 200
    assert "Cuestionario" in r.text and "ejercicio.py" in r.text


def test_capitulo_inexistente(cliente):
    assert cliente.get("/c/nada/nada").status_code == 404


def test_marcar_leido_alterna(cliente):
    assert "✓ Leído" in cliente.post(f"{URL}/leido").text
    assert "Marcar como leído" in cliente.post(f"{URL}/leido").text


def test_quiz_aprobado(cliente):
    r = cliente.post(f"{URL}/quiz", data=respuestas_correctas())
    assert r.status_code == 200
    assert "Aprobado" in r.text
    assert 'id="marca-quiz"' in r.text


def test_quiz_desaprobado_no_revela_explicaciones(cliente):
    r = cliente.post(f"{URL}/quiz", data={})
    assert "Necesitás" in r.text
    assert CAP.preguntas()[0].explicacion[:20] not in r.text


def test_tests_y_solucion(cliente):
    assert "se habilita" in cliente.get(f"{URL}/solucion").text

    r = cliente.post(f"{URL}/tests", data={"codigo": CAP.codigo_inicial()})
    assert "0 de" in r.text

    r = cliente.post(f"{URL}/tests", data={"codigo": CAP.solucion()})
    assert "Ejercicio aprobado" in r.text
    assert "<pre><code" in cliente.get(f"{URL}/solucion").text


def test_progreso_persiste_y_completa(cliente):
    cliente.post(f"{URL}/leido")
    cliente.post(f"{URL}/quiz", data=respuestas_correctas())
    cliente.post(f"{URL}/tests", data={"codigo": CAP.solucion()})
    # Un intento fallido posterior no borra lo aprobado.
    cliente.post(f"{URL}/tests", data={"codigo": CAP.codigo_inicial()})
    cliente.post(f"{URL}/quiz", data={})

    indice = cliente.get("/").text
    assert "capitulo-fila completo" in indice


def test_autoguardado(cliente):
    assert cliente.post(f"{URL}/codigo", data={"codigo": "# mi código"}).status_code == 204
    assert "# mi código" in cliente.get(URL).text
    assert cliente.get(f"{URL}/inicial").text == CAP.codigo_inicial()


def test_marcar_pasos_como_resueltos_completa_el_capitulo(cliente):
    cliente.post(f"{URL}/leido")
    r = cliente.post(f"{URL}/quiz/resuelto")
    assert "✓ Resuelto" in r.text and 'id="marca-quiz"' in r.text
    r = cliente.post(f"{URL}/tests/resuelto")
    assert "✓ Resuelto" in r.text and 'id="marca-tests"' in r.text
    assert "ver la solución de referencia" in r.text

    assert "capitulo-fila completo" in cliente.get("/").text
    assert "<pre><code" in cliente.get(f"{URL}/solucion").text


def test_marcar_resuelto_es_un_toggle(cliente):
    cliente.post(f"{URL}/tests/resuelto")
    r = cliente.post(f"{URL}/tests/resuelto")
    assert "Marcar como resuelto" in r.text
    assert "se habilita" in cliente.get(f"{URL}/solucion").text


def test_marcar_resuelto_paso_invalido(cliente):
    assert cliente.post(f"{URL}/leccion/resuelto").status_code == 422
