import ejercicio
import pytest
from ejercicio import Direccion, UsuarioNuevo, app
from fastapi.testclient import TestClient
from pydantic import ValidationError

VALIDO = {"nombre": "  Ana  ", "email": "ANA@Mail.com", "edad": 31, "password": "secreta123"}


@pytest.fixture
def cliente():
    ejercicio.USUARIOS.clear()
    return TestClient(app)


def test_normaliza_nombre_y_email():
    u = UsuarioNuevo(**VALIDO)
    assert u.nombre == "Ana"
    assert u.email == "ana@mail.com"


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("nombre", " A "),
        ("nombre", "x" * 51),
        ("email", "sin-arroba"),
        ("edad", -1),
        ("edad", 131),
        ("password", "corta"),
    ],
)
def test_rechaza_datos_invalidos(campo, valor):
    with pytest.raises(ValidationError) as info:
        UsuarioNuevo(**(VALIDO | {campo: valor}))
    assert info.value.errors()[0]["loc"] == (campo,)


def test_password_distinto_del_nombre():
    with pytest.raises(ValidationError, match="igual al nombre"):
        UsuarioNuevo(**(VALIDO | {"nombre": "Contraseña", "password": "CONTRASEÑA"}))


def test_direccion_anidada():
    with pytest.raises(ValidationError) as info:
        UsuarioNuevo(**VALIDO, direccion={"calle": "Mitre 123", "ciudad": "Rosario", "cp": "20"})
    assert info.value.errors()[0]["loc"] == ("direccion", "cp")
    assert Direccion(calle="Mitre 123", ciudad="Rosario", cp="2000").cp == "2000"


def test_api_crea_sin_exponer_password(cliente):
    r = cliente.post("/usuarios", json=VALIDO)
    assert r.status_code == 201
    assert r.json() == {"id": 1, "nombre": "Ana", "email": "ana@mail.com", "edad": 31}
    assert cliente.get("/usuarios/1").json()["email"] == "ana@mail.com"
    assert cliente.get("/usuarios/2").status_code == 404


def test_api_valida_el_body(cliente):
    r = cliente.post("/usuarios", json=VALIDO | {"edad": 200})
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "edad"]
