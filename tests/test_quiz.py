from app.contenido import Pregunta
from app.quiz import corregir

PREGUNTAS = [Pregunta(texto=f"p{i}", opciones=["a", "b"], correcta=1) for i in range(5)]


def test_todas_bien():
    r = corregir(PREGUNTAS, {i: 1 for i in range(5)})
    assert r.correctas == 5 and r.aprobado


def test_umbral_80_por_ciento():
    cuatro_de_cinco = corregir(PREGUNTAS, {0: 1, 1: 1, 2: 1, 3: 1, 4: 0})
    assert cuatro_de_cinco.aprobado
    tres_de_cinco = corregir(PREGUNTAS, {0: 1, 1: 1, 2: 1, 3: 0, 4: 0})
    assert not tres_de_cinco.aprobado


def test_sin_responder_cuenta_como_mal():
    r = corregir(PREGUNTAS, {0: 1})
    assert r.correctas == 1
    assert r.respuestas[1].elegida is None and not r.respuestas[1].ok


def test_sin_preguntas_no_aprueba():
    assert not corregir([], {}).aprobado
