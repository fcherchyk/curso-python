import inspect
import math
import os.path
import types

import exercise
import pytest
from exercise import import_object, installed_version, main, public_api


def test_import_object_with_colon():
    assert import_object("math:sqrt") is math.sqrt


def test_import_object_with_dot():
    assert import_object("os.path.join") is os.path.join


def test_import_object_missing_module():
    with pytest.raises(ImportError):
        import_object("this_module_does_not_exist.thing")


def test_public_api_without_all():
    m = types.ModuleType("fake")
    m.b = 1
    m.a = 2
    m._private = 3
    assert public_api(m) == ["a", "b"]


def test_public_api_with_all():
    m = types.ModuleType("fake")
    m.x = m.y = m.z = 1
    m.__all__ = ["z", "x"]
    assert public_api(m) == ["x", "z"]


def test_installed_version():
    v = installed_version("pytest")
    assert isinstance(v, str) and v[0].isdigit()
    assert installed_version("package-that-does-not-exist-123") is None


def test_main(capsys):
    assert main(["alice", "bob"]) == 0
    assert capsys.readouterr().out == "Hello, alice!\nHello, bob!\n"


def test_main_without_arguments(capsys):
    assert main([]) == 2
    assert "usage:" in capsys.readouterr().out


def test_has_main_guard():
    source = inspect.getsource(exercise)
    assert 'if __name__ == "__main__":' in source
