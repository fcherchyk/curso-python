import pytest
from exercise import ProductRepo, User, app, current_user, get_repo
from fastapi.testclient import TestClient

ALICE = {"Authorization": "Bearer t-alice"}
BOB = {"Authorization": "Bearer t-bob"}


@pytest.fixture
def repo():
    """Fake repository, injected with dependency_overrides."""
    fake = ProductRepo(["a", "b", "c", "d", "e"])
    app.dependency_overrides[get_repo] = lambda: fake
    yield fake
    app.dependency_overrides.clear()


@pytest.fixture
def client(repo):
    return TestClient(app)


def test_pagination(client):
    assert client.get("/products").json() == ["a", "b", "c", "d", "e"]
    r = client.get("/products", params={"page": 2, "per_page": 2})
    assert r.json() == ["c", "d"]


def test_pagination_validates(client):
    assert client.get("/products", params={"page": 0}).status_code == 422
    assert client.get("/products", params={"per_page": 51}).status_code == 422


def test_me(client):
    assert client.get("/me", headers=BOB).json() == {"name": "bob", "is_admin": False}


def test_missing_or_invalid_token(client):
    r = client.get("/me")
    assert r.status_code == 401
    assert r.json() == {"detail": "missing token"}
    assert r.headers["WWW-Authenticate"] == "Bearer"
    r = client.get("/me", headers={"Authorization": "Bearer nothing"})
    assert r.status_code == 401
    assert r.json() == {"detail": "invalid token"}


def test_delete_requires_admin(client, repo):
    assert client.delete("/products/0", headers=BOB).status_code == 403
    assert client.delete("/products/0").status_code == 401
    assert client.delete("/products/0", headers=ALICE).status_code == 204
    assert repo.products == ["b", "c", "d", "e"]
    assert client.delete("/products/99", headers=ALICE).status_code == 404


def test_user_override(client):
    app.dependency_overrides[current_user] = lambda: User("tester", is_admin=True)
    assert client.get("/me").json() == {"name": "tester", "is_admin": True}
    assert client.delete("/products/1").status_code == 204, "admin_only depends on current_user"
