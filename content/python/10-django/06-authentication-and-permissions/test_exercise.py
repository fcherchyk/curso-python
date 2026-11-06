import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="exercise",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth", "django.contrib.sessions"],
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
    LOGIN_URL="/login/",
    USE_TZ=True,
)
django.setup()

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from django.test import Client
from exercise import Nota, registrar

User = get_user_model()
call_command("migrate", verbosity=0)  # tablas de auth, contenttypes y sessions


@pytest.fixture(autouse=True)
def tablas():
    with connection.schema_editor() as editor:
        editor.create_model(Nota)
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Nota)
    User.objects.all().delete()


def logueado(username: str, staff: bool = False) -> Client:
    u = User.objects.create_user(username, password="x", is_staff=staff)
    c = Client()
    c.force_login(u)
    return c


def test_registrar_hashea():
    u = registrar("ana", "clave-segura")
    assert u.password != "clave-segura"
    assert u.check_password("clave-segura")
    with pytest.raises(ValueError, match="usuario existente"):
        registrar("ana", "otra")


def test_login_y_logout():
    User.objects.create_user("ana", password="clave")
    c = Client()
    r = c.post("/login/", {"username": "ana", "password": "mala"})
    assert r.status_code == 400
    assert r.json() == {"error": "credenciales inválidas"}
    assert c.post("/login/", {"username": "ana", "password": "clave"}).status_code == 204
    assert c.get("/notas/").status_code == 200, "después del login, la sesión lo identifica"
    assert c.post("/logout/").status_code == 204
    assert c.get("/notas/").status_code == 302


def test_notas_requiere_login():
    r = Client().get("/notas/")
    assert r.status_code == 302
    assert r.headers["Location"] == "/login/?next=/notas/"


def test_notas_privadas_por_usuario():
    ana, beto = logueado("ana"), logueado("beto")
    r = ana.post("/notas/", {"texto": "de ana"})
    assert r.status_code == 201
    assert r.json()["texto"] == "de ana"
    beto.post("/notas/", {"texto": "de beto"})
    assert [n["texto"] for n in ana.get("/notas/").json()] == ["de ana"]
    assert [n["texto"] for n in beto.get("/notas/").json()] == ["de beto"]


def test_borrar_solo_dueno_o_staff():
    ana, beto, jefa = logueado("ana"), logueado("beto"), logueado("jefa", staff=True)
    id_ana = ana.post("/notas/", {"texto": "x"}).json()["id"]
    assert beto.delete(f"/notas/{id_ana}/").status_code == 403
    assert jefa.delete(f"/notas/{id_ana}/").status_code == 204
    id2 = ana.post("/notas/", {"texto": "y"}).json()["id"]
    assert ana.delete(f"/notas/{id2}/").status_code == 204
    assert ana.delete("/notas/999/").status_code == 404
    assert Nota.objects.count() == 0
