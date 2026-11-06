import pytest
from exercise import Temperature, User


def test_temperature_celsius_and_fahrenheit():
    t = Temperature(100)
    assert t.celsius == 100
    assert t.fahrenheit == 212


def test_temperature_fahrenheit_setter_updates_celsius():
    t = Temperature(0)
    t.fahrenheit = 50
    assert t.celsius == pytest.approx(10)


def test_temperature_validates_on_construction_and_assignment():
    with pytest.raises(ValueError):
        Temperature(-300)
    t = Temperature(20)
    with pytest.raises(ValueError):
        t.celsius = -274


def test_temperature_from_fahrenheit():
    t = Temperature.from_fahrenheit(32)
    assert isinstance(t, Temperature)
    assert t.celsius == pytest.approx(0)


def test_from_fahrenheit_respects_subclasses():
    class RoomTemperature(Temperature):
        pass

    assert type(RoomTemperature.from_fahrenheit(68)) is RoomTemperature


def test_user_email_normalized():
    u = User(1, "  Alice@Mail.COM ")
    assert u.email == "alice@mail.com"
    u.email = "BOB@x.org"
    assert u.email == "bob@x.org"


def test_user_invalid_email():
    with pytest.raises(ValueError):
        User(1, "no-at-sign")
    u = User(1, "a@b.c")
    with pytest.raises(ValueError):
        u.email = "nope"


def test_user_id_read_only():
    u = User(7, "a@b.c")
    assert u.id == 7
    with pytest.raises(AttributeError):
        u.id = 8


def test_user_normalize_email_is_static():
    assert User.normalize_email(" X@Y.Z ") == "x@y.z"


def test_user_from_dict():
    u = User.from_dict({"id": 3, "email": "C@D.E"})
    assert (u.id, u.email) == (3, "c@d.e")
