import pytest
from ejercicio import Circulo, Rectangulo, describir_figura, interpretar_comando, procesar_evento


@pytest.mark.parametrize(
    ("comando", "esperado"),
    [
        ("salir", "chau"),
        ("quit", "chau"),
        ("ir norte", "yendo a norte"),
        ("ir arriba", "dirección inválida"),
        ("tomar espada", "tomaste: espada"),
        ("tomar espada escudo", "tomaste: espada, escudo"),
        ("tomar", "no entiendo"),
        ("", "decí algo"),
        ("bailar tango", "no entiendo"),
        ("salir ya", "no entiendo"),
    ],
)
def test_interpretar_comando(comando, esperado):
    assert interpretar_comando(comando) == esperado


@pytest.mark.parametrize(
    ("evento", "esperado"),
    [
        ({"tipo": "click", "x": 10, "y": 20}, "click en (10, 20)"),
        ({"tipo": "click", "x": 1, "y": 2, "boton": "izq"}, "click en (1, 2)"),
        ({"tipo": "click", "x": "10", "y": 20}, "desconocido"),
        ({"tipo": "tecla", "tecla": "enter"}, "confirmar"),
        ({"tipo": "tecla", "tecla": "a"}, "tecla a"),
        ({"tipo": "scroll", "delta": -3}, "scroll abajo"),
        ({"tipo": "scroll", "delta": 2}, "scroll arriba"),
        ({"tipo": "scroll", "delta": 0}, "desconocido"),
        ({"otro": 1}, "desconocido"),
    ],
)
def test_procesar_evento(evento, esperado):
    assert procesar_evento(evento) == esperado


def test_describir_figura():
    assert describir_figura(Circulo(2)) == "círculo de radio 2"
    assert describir_figura(Rectangulo(3, 3)) == "cuadrado de lado 3"
    assert describir_figura(Rectangulo(2, 5)) == "rectángulo 2 x 5"
    assert describir_figura(Circulo(0)) == "degenerada"
    assert describir_figura(Rectangulo(0, 4)) == "degenerada"


def test_describir_figura_desconocida():
    with pytest.raises(TypeError):
        describir_figura("triángulo")
