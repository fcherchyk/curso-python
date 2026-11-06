import exercise
import pytest
from exercise import Address, NewUser, app
from fastapi.testclient import TestClient
from pydantic import ValidationError

VALID = {"name": "  Alice  ", "email": "ALICE@Mail.com", "age": 31, "password": "secret123"}


@pytest.fixture
def client():
    exercise.USERS.clear()
    return TestClient(app)


def test_normalizes_name_and_email():
    u = NewUser(**VALID)
    assert u.name == "Alice"
    assert u.email == "alice@mail.com"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", " A "),
        ("name", "x" * 51),
        ("email", "no-at-sign"),
        ("age", -1),
        ("age", 131),
        ("password", "short"),
    ],
)
def test_rejects_invalid_data(field, value):
    with pytest.raises(ValidationError) as info:
        NewUser(**(VALID | {field: value}))
    assert info.value.errors()[0]["loc"] == (field,)


def test_password_differs_from_name():
    with pytest.raises(ValidationError, match="same as the name"):
        NewUser(**(VALID | {"name": "Password", "password": "PASSWORD"}))


def test_nested_address():
    with pytest.raises(ValidationError) as info:
        NewUser(**VALID, address={"street": "Main St 123", "city": "Springfield", "postcode": "20"})
    assert info.value.errors()[0]["loc"] == ("address", "postcode")
    assert Address(street="Main St 123", city="Springfield", postcode="2000").postcode == "2000"


def test_api_creates_without_exposing_password(client):
    r = client.post("/users", json=VALID)
    assert r.status_code == 201
    assert r.json() == {"id": 1, "name": "Alice", "email": "alice@mail.com", "age": 31}
    assert client.get("/users/1").json()["email"] == "alice@mail.com"
    assert client.get("/users/2").status_code == 404


def test_api_validates_the_body(client):
    r = client.post("/users", json=VALID | {"age": 200})
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "age"]
