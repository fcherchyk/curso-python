import pytest
from exercise import (
    ConfigError,
    InsufficientFunds,
    process_all,
    read_config,
    to_int,
    withdraw,
)


def test_to_int():
    assert to_int(" 42 ") == 42
    assert to_int("-7") == -7
    assert to_int("4.2", default=-1) == -1
    assert to_int("abc") is None


def test_withdraw_ok():
    assert withdraw(100, 30) == 70
    assert withdraw(100, 100) == 0


def test_withdraw_invalid_amount():
    with pytest.raises(ValueError):
        withdraw(100, 0)
    with pytest.raises(ValueError):
        withdraw(100, -5)


def test_withdraw_insufficient_funds():
    with pytest.raises(InsufficientFunds) as info:
        withdraw(50, 80)
    assert info.value.balance == 50
    assert info.value.amount == 80
    assert "50" in str(info.value) and "80" in str(info.value)


def test_read_config(tmp_path):
    path = tmp_path / "app.cfg"
    path.write_text("host=db.local\n\nport=5432\n")
    assert read_config(path) == {"host": "db.local", "port": "5432"}


def test_read_config_missing_file_chains(tmp_path):
    with pytest.raises(ConfigError) as info:
        read_config(tmp_path / "does-not-exist.cfg")
    assert isinstance(info.value.__cause__, FileNotFoundError)


def test_process_all():
    assert process_all(["1", "x", "3", "", "-2"]) == ([1, 3, -2], ["x", ""])
    assert process_all([]) == ([], [])
