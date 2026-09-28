import io

import pytest

from semana1.dia5_novedades.ejercicios import (
    DEFAULTS,
    Circulo,
    Rectangulo,
    cargar_config,
    clasificar_errores,
    describir_figura,
    interpretar_comando,
    largos_mayores,
    leer_en_bloques,
    procesar_evento,
    tabla_precios,
    validar_usuario,
)


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
    with pytest.raises(TypeError):
        describir_figura("triángulo")


def test_leer_en_bloques():
    assert leer_en_bloques(io.StringIO("abcdefg"), 3) == ["abc", "def", "g"]
    assert leer_en_bloques(io.StringIO(""), 3) == []


def test_largos_mayores():
    assert largos_mayores(["a", "hola", "mundo", "yo"], 2) == [4, 5]


def test_validar_usuario_ok():
    validar_usuario({"nombre": "Ana", "edad": 30, "email": "a@b.com"})


def test_validar_usuario_reporta_todo():
    with pytest.raises(ExceptionGroup) as info:
        validar_usuario({"nombre": "", "edad": "treinta", "email": "sin-arroba"})
    mensajes = sorted(str(e) for e in info.value.exceptions)
    assert mensajes == ["edad", "email", "nombre"]


def test_clasificar_errores():
    assert clasificar_errores({"nombre": "", "edad": -1, "email": "x"}) == {
        "valor": ["nombre", "edad", "email"],
        "tipo": [],
    }
    assert clasificar_errores({"nombre": "A", "edad": "x", "email": "a@b"}) == {
        "valor": [],
        "tipo": ["edad"],
    }
    assert clasificar_errores({"nombre": "A", "edad": 1, "email": "a@b"}) == {
        "valor": [],
        "tipo": [],
    }


def test_tabla_precios():
    tabla = tabla_precios([("café", 1500.5), ("medialunas", 12.0)])
    assert tabla == ("café          1,500.50\nmedialunas       12.00\nTOTAL         1,512.50")


def test_cargar_config():
    toml = """
    [server]
    host = "https://api.ejemplo.com"
    port = 9000
    """
    assert cargar_config(toml) == {"host": "api.ejemplo.com", "port": 9000, "debug": False}


def test_cargar_config_sin_seccion_no_muta_defaults():
    config = cargar_config('titulo = "x"')
    assert config == DEFAULTS
    config["port"] = 1
    assert DEFAULTS["port"] == 8000
