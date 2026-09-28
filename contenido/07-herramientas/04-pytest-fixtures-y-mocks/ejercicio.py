"""Escribí TESTS para clima.py (el código está en la lección).

Requisitos:
- al menos 4 funciones de test
- al menos una fixture propia (`@pytest.fixture`)
- usar `Mock` (de unittest.mock) y la fixture `tmp_path`
- tienen que pasar con el código correcto y detectar los 4 mutantes
"""

from unittest.mock import Mock  # noqa: F401

import pytest  # noqa: F401
from clima import BASE, guardar_reporte, resumen, temperatura  # noqa: F401


def test_temperatura():
    raise NotImplementedError("TODO: escribí el test")
