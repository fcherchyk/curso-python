"""property, classmethod y staticmethod."""

from typing import Any

CERO_ABSOLUTO = -273.15


class Temperatura:
    """Temperatura con dos vistas: celsius y fahrenheit.

    - `celsius`: property con setter; debajo del cero absoluto → ValueError
      (también al construir).
    - `fahrenheit`: property calculada CON setter (asignarla actualiza celsius).
    - `Temperatura.desde_fahrenheit(f)`: constructor alternativo.
    """

    def __init__(self, celsius: float) -> None:
        raise NotImplementedError("TODO")

    # Completá: property celsius (+ setter), property fahrenheit (+ setter)
    # y el classmethod desde_fahrenheit.


class Usuario:
    """Usuario con:

    - `id`: de solo lectura (property sin setter).
    - `email`: property; al asignar se normaliza (strip + minúsculas) y, si no tiene
      "@", ValueError.
    - `Usuario.normalizar_email(texto)`: staticmethod que hace la normalización.
    - `Usuario.desde_dict({"id": 1, "email": "..."})`: classmethod.
    """

    def __init__(self, id: int, email: str) -> None:
        raise NotImplementedError("TODO")

    @staticmethod
    def normalizar_email(texto: str) -> str:
        raise NotImplementedError("TODO")

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> "Usuario":
        raise NotImplementedError("TODO")
