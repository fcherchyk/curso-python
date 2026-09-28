import pytest
from ejercicio import (
    ConfigError,
    SaldoInsuficiente,
    a_entero,
    leer_config,
    procesar_todos,
    retirar,
)


def test_a_entero():
    assert a_entero(" 42 ") == 42
    assert a_entero("-7") == -7
    assert a_entero("4.2", default=-1) == -1
    assert a_entero("abc") is None


def test_retirar_ok():
    assert retirar(100, 30) == 70
    assert retirar(100, 100) == 0


def test_retirar_monto_invalido():
    with pytest.raises(ValueError):
        retirar(100, 0)
    with pytest.raises(ValueError):
        retirar(100, -5)


def test_retirar_saldo_insuficiente():
    with pytest.raises(SaldoInsuficiente) as info:
        retirar(50, 80)
    assert info.value.saldo == 50
    assert info.value.monto == 80
    assert "50" in str(info.value) and "80" in str(info.value)


def test_leer_config(tmp_path):
    ruta = tmp_path / "app.cfg"
    ruta.write_text("host=db.local\n\nport=5432\n")
    assert leer_config(ruta) == {"host": "db.local", "port": "5432"}


def test_leer_config_inexistente_encadena(tmp_path):
    with pytest.raises(ConfigError) as info:
        leer_config(tmp_path / "no-existe.cfg")
    assert isinstance(info.value.__cause__, FileNotFoundError)


def test_procesar_todos():
    assert procesar_todos(["1", "x", "3", "", "-2"]) == ([1, 3, -2], ["x", ""])
    assert procesar_todos([]) == ([], [])
