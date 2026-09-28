import time
from pathlib import Path

import pytest

from semana1.dia3_funciones.ejercicios import (
    Temporizador,
    capturar_errores,
    componer,
    contar_llamadas,
    crear_contador,
    en_directorio,
    memoizar,
    reintentar,
)


def test_crear_contador_independientes():
    a, b = crear_contador(), crear_contador(10)
    assert [a(), a(), a()] == [0, 1, 2]
    assert [b(), b()] == [10, 11]
    assert a() == 3


def test_componer():
    def doble(x):
        return x * 2

    def mas_uno(x):
        return x + 1

    assert componer(doble, mas_uno)(3) == 8  # doble(mas_uno(3))
    assert componer(mas_uno, doble)(3) == 7
    assert componer()(42) == 42


def test_contar_llamadas():
    @contar_llamadas
    def saludar(nombre):
        """Saluda."""
        return f"hola {nombre}"

    assert saludar.llamadas == 0
    assert saludar("ana") == "hola ana"
    saludar(nombre="beto")
    assert saludar.llamadas == 2
    assert saludar.__name__ == "saludar"
    assert saludar.__doc__ == "Saluda."


def test_reintentar_hasta_exito():
    intentos = []

    @reintentar(3, excepciones=(ConnectionError,))
    def inestable():
        intentos.append(1)
        if len(intentos) < 3:
            raise ConnectionError
        return "ok"

    assert inestable() == "ok"
    assert len(intentos) == 3


def test_reintentar_agota_y_relevanta():
    intentos = []

    @reintentar(2)
    def siempre_falla():
        intentos.append(1)
        raise ValueError("nop")

    with pytest.raises(ValueError, match="nop"):
        siempre_falla()
    assert len(intentos) == 2


def test_reintentar_no_captura_otras():
    intentos = []

    @reintentar(5, excepciones=(ConnectionError,))
    def falla_distinto():
        intentos.append(1)
        raise KeyError

    with pytest.raises(KeyError):
        falla_distinto()
    assert len(intentos) == 1


def test_memoizar():
    llamadas = []

    @memoizar
    def lento(a, b):
        llamadas.append((a, b))
        return a + b

    assert lento(1, 2) == 3
    assert lento(1, 2) == 3
    assert lento(2, 1) == 3
    assert llamadas == [(1, 2), (2, 1)]
    assert len(lento.cache) == 2


def test_memoizar_fibonacci_rapido():
    @memoizar
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(80) == 23416728348467685


def test_temporizador():
    t = Temporizador()
    assert t.duracion is None
    with t as mismo:
        assert mismo is t
        time.sleep(0.01)
    assert 0.005 < t.duracion < 1


def test_temporizador_no_suprime():
    t = Temporizador()
    with pytest.raises(RuntimeError), t:
        raise RuntimeError
    assert t.duracion is not None


def test_en_directorio(tmp_path):
    original = Path.cwd()
    with en_directorio(tmp_path) as p:
        assert Path.cwd() == tmp_path.resolve()
        assert p == tmp_path
    assert Path.cwd() == original


def test_en_directorio_restaura_con_excepcion(tmp_path):
    original = Path.cwd()
    with pytest.raises(ZeroDivisionError), en_directorio(tmp_path):
        1 / 0
    assert Path.cwd() == original


def test_capturar_errores():
    with capturar_errores(ValueError, KeyError) as errores:
        int("no es número")
    assert len(errores) == 1
    assert isinstance(errores[0], ValueError)

    with capturar_errores(ValueError) as errores:
        pass
    assert errores == []

    with pytest.raises(TypeError), capturar_errores(ValueError):
        raise TypeError
