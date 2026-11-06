import io

from exercise import extraer_precios, largos_mayores, leer_en_bloques, primer_ok


def test_leer_en_bloques():
    assert leer_en_bloques(io.StringIO("abcdefg"), 3) == ["abc", "def", "g"]
    assert leer_en_bloques(io.StringIO(""), 3) == []


def test_largos_mayores():
    assert largos_mayores(["a", "hola", "mundo", "yo"], 2) == [4, 5]


def test_extraer_precios():
    assert extraer_precios(["café $ 2.5", "sin precio", "pan $3", "$ 10.25 total"]) == [
        2.5,
        3.0,
        10.25,
    ]


def test_primer_ok():
    respuestas = iter([None, None, "ok", "otro"])
    llamadas = []

    def intento():
        llamadas.append(1)
        return next(respuestas)

    assert primer_ok(intento, 5) == "ok"
    assert len(llamadas) == 3


def test_primer_ok_agota():
    llamadas = []

    def falla():
        llamadas.append(1)
        return None

    assert primer_ok(falla, 4) is None
    assert len(llamadas) == 4
