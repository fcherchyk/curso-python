"""Valida todo el temario: cada capítulo tiene que estar completo y ser coherente."""

import pytest

from app.contenido import cargar_cursos
from app.render import markdown

CURSOS = cargar_cursos()
CAPITULOS = [c for curso in CURSOS for c in curso.capitulos()]


def test_hay_contenido():
    assert CAPITULOS
    assert "python" in {c.slug for c in CURSOS}


@pytest.mark.parametrize("cap", CAPITULOS, ids=lambda c: c.id)
def test_capitulo_tiene_todos_los_archivos(cap):
    lenguaje = cap.lenguaje
    for nombre in (
        "leccion.md",
        "quiz.toml",
        lenguaje.archivo_ejercicio,
        lenguaje.archivo_tests,
        lenguaje.archivo_solucion,
    ):
        assert (cap.ruta / nombre).exists(), f"falta {nombre}"
    assert cap.titulo != cap.slug, "leccion.md tiene que empezar con '# Título'"


@pytest.mark.parametrize("cap", CAPITULOS, ids=lambda c: c.id)
def test_leccion_renderiza(cap):
    html = markdown(cap.leccion())
    assert "<h2>" in html


@pytest.mark.parametrize("cap", CAPITULOS, ids=lambda c: c.id)
def test_quiz_valido(cap):
    preguntas = cap.preguntas()
    assert len(preguntas) >= 4
    for p in preguntas:
        assert p.texto and p.explicacion
        assert len(p.opciones) >= 2
        assert 0 <= p.correcta < len(p.opciones)
        assert len(set(p.opciones)) == len(p.opciones), "opciones repetidas"


@pytest.mark.parametrize("cap", CAPITULOS, ids=lambda c: c.id)
def test_solucion_pasa_los_tests(cap):
    resultado = cap.lenguaje.correr(cap.solucion(), cap.archivos_de_soporte())
    assert resultado.error is None, resultado.error
    fallidos = [t for t in resultado.tests if not t.ok]
    assert not fallidos, "\n\n".join(f"{t.nombre}\n{t.mensaje}" for t in fallidos)


@pytest.mark.parametrize("cap", CAPITULOS, ids=lambda c: c.id)
def test_ejercicio_inicial_no_pasa(cap):
    resultado = cap.lenguaje.correr(cap.codigo_inicial(), cap.archivos_de_soporte())
    assert resultado.error is None, f"el código inicial tiene que compilar: {resultado.error}"
    # Cada test tiene que fallar sin resolver el ejercicio.
    aprobados = [t.nombre for t in resultado.tests if t.ok]
    assert not aprobados, f"estos tests pasan sin resolver el ejercicio: {aprobados}"
