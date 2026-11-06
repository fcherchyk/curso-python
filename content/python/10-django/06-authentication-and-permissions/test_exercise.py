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
from exercise import Note, register

User = get_user_model()
call_command("migrate", verbosity=0)  # auth, contenttypes and sessions tables


@pytest.fixture(autouse=True)
def tables():
    with connection.schema_editor() as editor:
        editor.create_model(Note)
    yield
    with connection.schema_editor() as editor:
        editor.delete_model(Note)
    User.objects.all().delete()


def logged_in(username: str, staff: bool = False) -> Client:
    u = User.objects.create_user(username, password="x", is_staff=staff)
    c = Client()
    c.force_login(u)
    return c


def test_register_hashes():
    u = register("alice", "secure-password")
    assert u.password != "secure-password"
    assert u.check_password("secure-password")
    with pytest.raises(ValueError, match="user already exists"):
        register("alice", "other")


def test_login_and_logout():
    User.objects.create_user("alice", password="secret")
    c = Client()
    r = c.post("/login/", {"username": "alice", "password": "wrong"})
    assert r.status_code == 400
    assert r.json() == {"error": "invalid credentials"}
    assert c.post("/login/", {"username": "alice", "password": "secret"}).status_code == 204
    assert c.get("/notes/").status_code == 200, "after login, the session identifies the user"
    assert c.post("/logout/").status_code == 204
    assert c.get("/notes/").status_code == 302


def test_notes_requires_login():
    r = Client().get("/notes/")
    assert r.status_code == 302
    assert r.headers["Location"] == "/login/?next=/notes/"


def test_notes_private_per_user():
    alice, bob = logged_in("alice"), logged_in("bob")
    r = alice.post("/notes/", {"text": "from alice"})
    assert r.status_code == 201
    assert r.json()["text"] == "from alice"
    bob.post("/notes/", {"text": "from bob"})
    assert [n["text"] for n in alice.get("/notes/").json()] == ["from alice"]
    assert [n["text"] for n in bob.get("/notes/").json()] == ["from bob"]


def test_delete_only_owner_or_staff():
    alice, bob, carol = logged_in("alice"), logged_in("bob"), logged_in("carol", staff=True)
    alice_id = alice.post("/notes/", {"text": "x"}).json()["id"]
    assert bob.delete(f"/notes/{alice_id}/").status_code == 403
    assert carol.delete(f"/notes/{alice_id}/").status_code == 204
    id2 = alice.post("/notes/", {"text": "y"}).json()["id"]
    assert alice.delete(f"/notes/{id2}/").status_code == 204
    assert alice.delete("/notes/999/").status_code == 404
    assert Note.objects.count() == 0
