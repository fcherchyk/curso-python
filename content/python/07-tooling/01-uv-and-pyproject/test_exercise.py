import pytest
from exercise import dependencias, grupos, nombre_de_paquete, python_minimo

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
    ("spec", "nombre"),
    [
        ("fastapi>=0.115", "fastapi"),
        ("httpx[http2]>=0.27", "httpx"),
        ("Pydantic >=2,<3", "pydantic"),
        ("uvicorn[standard]", "uvicorn"),
        ("mkdocs-material==9.*", "mkdocs-material"),
        ("zope.interface", "zope.interface"),
    ],
)
def test_nombre_de_paquete(spec, nombre):
    assert nombre_de_paquete(spec) == nombre


def test_dependencias():
    assert dependencias(PYPROJECT) == ["fastapi", "httpx", "pydantic", "uvicorn"]
    assert dependencias('[project]\nname = "x"') == []


def test_grupos():
    assert grupos(PYPROJECT) == {"dev": ["pytest", "ruff"], "docs": ["mkdocs-material"]}
    assert grupos("") == {}


def test_python_minimo():
    assert python_minimo(PYPROJECT) == (3, 12)
    assert python_minimo('[project]\nname = "x"') is None
