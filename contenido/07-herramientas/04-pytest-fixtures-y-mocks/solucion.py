"""Tests de referencia para clima.py."""

from unittest.mock import Mock

import pytest
from clima import BASE, guardar_reporte, resumen, temperatura


@pytest.fixture
def cliente():
    """Cliente falso: responde según la ciudad de la URL; "Atlantis" no existe."""
    datos = {"Rosario": 21.456, "Salta": 18.04}

    def responder(url: str):
        ciudad = url.rsplit("=", 1)[-1]
        if ciudad not in datos:
            raise KeyError(ciudad)
        return {"temp_c": datos[ciudad]}

    return Mock(get_json=Mock(side_effect=responder))


def test_temperatura_redondea(cliente):
    assert temperatura("Rosario", cliente) == 21.5


def test_temperatura_pide_la_url_de_la_ciudad():
    c = Mock()
    c.get_json.return_value = {"temp_c": 10}
    temperatura("Salta", c)
    c.get_json.assert_called_once_with(f"{BASE}/actual?ciudad=Salta")


def test_resumen_omite_las_que_fallan(cliente):
    assert resumen(["Rosario", "Atlantis", "Salta"], cliente) == {"Rosario": 21.5, "Salta": 18.0}


def test_guardar_reporte_ordenado(tmp_path):
    ruta = tmp_path / "reporte.txt"
    guardar_reporte(ruta, {"Salta": 18.0, "Rosario": 21.5})
    assert ruta.read_text(encoding="utf-8") == "Rosario: 21.5\nSalta: 18.0\n"
