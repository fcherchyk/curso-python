import inspect
import math
import os.path
import types

import exercise
import pytest
from exercise import api_publica, importar, main, version_instalada


def test_importar_con_dos_puntos():
    assert importar("math:sqrt") is math.sqrt


def test_importar_con_punto():
    assert importar("os.path.join") is os.path.join


def test_importar_modulo_inexistente():
    with pytest.raises(ImportError):
        importar("no_existe_este_modulo.cosa")


def test_api_publica_sin_all():
    m = types.ModuleType("falso")
    m.b = 1
    m.a = 2
    m._privado = 3
    assert api_publica(m) == ["a", "b"]


def test_api_publica_con_all():
    m = types.ModuleType("falso")
    m.x = m.y = m.z = 1
    m.__all__ = ["z", "x"]
    assert api_publica(m) == ["x", "z"]


def test_version_instalada():
    v = version_instalada("pytest")
    assert isinstance(v, str) and v[0].isdigit()
    assert version_instalada("paquete-que-no-existe-123") is None


def test_main(capsys):
    assert main(["ana", "beto"]) == 0
    assert capsys.readouterr().out == "Hola, ana!\nHola, beto!\n"


def test_main_sin_argumentos(capsys):
    assert main([]) == 2
    assert "uso:" in capsys.readouterr().out


def test_tiene_guarda_main():
    fuente = inspect.getsource(exercise)
    assert 'if __name__ == "__main__":' in fuente
