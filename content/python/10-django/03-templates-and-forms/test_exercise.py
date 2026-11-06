import django
from django.conf import settings

settings.configure(
    SECRET_KEY="tests",
    DEBUG=True,
    ROOT_URLCONF="exercise",
    ALLOWED_HOSTS=["testserver"],
    INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
    MIDDLEWARE=["django.middleware.csrf.CsrfViewMiddleware"],
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": ["templates"]}],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    USE_TZ=True,
)
django.setup()

import re

import exercise
import pytest
from django.test import Client
from exercise import ContactForm

VALID = {"name": "  alice smith ", "email": "alice@x.com", "message": "Hi, I'd like some info"}


@pytest.fixture(autouse=True)
def clear():
    exercise.MESSAGES.clear()


def test_valid_form_cleans_the_name():
    form = ContactForm(data=VALID)
    assert form.is_valid(), form.errors
    assert form.cleaned_data["name"] == "Alice Smith"


def test_form_errors_per_field():
    form = ContactForm(data={"name": "x" * 51, "email": "not-an-email", "message": "short"})
    assert not form.is_valid()
    assert set(form.errors) == {"name", "email", "message"}


def test_form_general_rule():
    form = ContactForm(data=VALID | {"message": "Buy cheap SPAM now"})
    assert not form.is_valid()
    assert form.non_field_errors() == ["The message looks like spam"]


def test_get_shows_the_form():
    r = Client().get("/contact/")
    assert r.status_code == 200
    html = r.content.decode()
    assert "<title>Contact</title>" in html
    assert 'name="email"' in html and "csrfmiddlewaretoken" in html


def test_valid_post_redirects_and_thanks():
    c = Client()
    r = c.post("/contact/", VALID)
    assert r.status_code == 302
    assert r.headers["Location"] == "/thanks/"
    assert exercise.MESSAGES[0]["name"] == "Alice Smith"
    html = c.get("/thanks/").content.decode()
    assert "Thanks, Alice Smith!" in html
    assert "We received 1 message." in html


def test_invalid_post_shows_errors():
    r = Client().post("/contact/", VALID | {"email": "bad"})
    assert r.status_code == 200
    assert 'data-field="email"' in r.content.decode()
    assert exercise.MESSAGES == []


def test_csrf():
    c = Client(enforce_csrf_checks=True)
    assert c.post("/contact/", VALID).status_code == 403
    token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', c.get("/contact/").content.decode())
    assert token, "the template has {% csrf_token %}: render with render(request, ...)"
    r = c.post("/contact/", VALID | {"csrfmiddlewaretoken": token.group(1)})
    assert r.status_code == 302
