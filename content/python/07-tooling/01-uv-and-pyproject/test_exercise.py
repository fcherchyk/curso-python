import pytest
from exercise import dependencies, groups, min_python, package_name

PYPROJECT = """
[project]
name = "demo"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "httpx[http2]>=0.27",
    "Pydantic >=2,<3",
    "uvicorn[standard]",
]

[dependency-groups]
dev = ["pytest>=8", "ruff~=0.6"]
docs = ["mkdocs-material==9.*"]

[tool.ruff]
line-length = 100
"""


@pytest.mark.parametrize(
    ("spec", "name"),
    [
        ("fastapi>=0.115", "fastapi"),
        ("httpx[http2]>=0.27", "httpx"),
        ("Pydantic >=2,<3", "pydantic"),
        ("uvicorn[standard]", "uvicorn"),
        ("mkdocs-material==9.*", "mkdocs-material"),
        ("zope.interface", "zope.interface"),
    ],
)
def test_package_name(spec, name):
    assert package_name(spec) == name


def test_dependencies():
    assert dependencies(PYPROJECT) == ["fastapi", "httpx", "pydantic", "uvicorn"]
    assert dependencies('[project]\nname = "x"') == []


def test_groups():
    assert groups(PYPROJECT) == {"dev": ["pytest", "ruff"], "docs": ["mkdocs-material"]}
    assert groups("") == {}


def test_min_python():
    assert min_python(PYPROJECT) == (3, 12)
    assert min_python('[project]\nname = "x"') is None
