import pytest
from ejercicio import clasificar_errores, ejecutar_todas, validar_usuario


def test_validar_usuario_ok():
    assert validar_usuario({"nombre": "Ana", "edad": 30, "email": "a@b.com"}) is None


def test_validar_usuario_reporta_todo():
    with pytest.raises(ExceptionGroup) as info:
        validar_usuario({"nombre": "", "edad": "treinta", "email": "sin-arroba"})
    mensajes = sorted(str(e) for e in info.value.exceptions)
    assert mensajes == ["edad", "email", "nombre"]


def test_validar_usuario_campos_faltantes():
    with pytest.raises(ExceptionGroup) as info:
        validar_usuario({})
    assert len(info.value.exceptions) == 3


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


def test_ejecutar_todas_sin_errores():
    assert ejecutar_todas([lambda: 1, lambda: "dos"]) == [1, "dos"]


def test_ejecutar_todas_junta_errores_con_notas():
    corridas = []

    def ok():
        corridas.append("ok")
        return 1

    def boom():
        raise KeyError("x")

    def otra():
        raise ValueError("y")

    with pytest.raises(ExceptionGroup) as info:
        ejecutar_todas([boom, ok, otra])
    assert corridas == ["ok"], "tiene que ejecutar todas aunque alguna falle"
    excs = info.value.exceptions
    assert [type(e) for e in excs] == [KeyError, ValueError]
    assert excs[0].__notes__ == ["tarea 0"]
    assert excs[1].__notes__ == ["tarea 2"]
