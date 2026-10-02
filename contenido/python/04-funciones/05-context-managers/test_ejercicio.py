import time
from pathlib import Path

import pytest
from ejercicio import Temporizador, capturar_errores, en_directorio


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
        _ = 1 / 0
    assert Path.cwd() == original


def test_capturar_errores():
    with capturar_errores(ValueError, KeyError) as errores:
        int("no es número")
    assert len(errores) == 1
    assert isinstance(errores[0], ValueError)


def test_capturar_errores_sin_error():
    with capturar_errores(ValueError) as errores:
        pass
    assert errores == []


def test_capturar_errores_propaga_otros():
    with pytest.raises(TypeError), capturar_errores(ValueError):
        raise TypeError
