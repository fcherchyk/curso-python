from typing import Any

CERO_ABSOLUTO = -273.15


class Temperatura:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius  # pasa por el setter: valida al construir

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, valor: float) -> None:
        if valor < CERO_ABSOLUTO:
            raise ValueError(f"debajo del cero absoluto: {valor}")
        self._celsius = valor

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, valor: float) -> None:
        self.celsius = (valor - 32) * 5 / 9

    @classmethod
    def desde_fahrenheit(cls, f: float) -> "Temperatura":
        return cls((f - 32) * 5 / 9)


class Usuario:
    def __init__(self, id: int, email: str) -> None:
        self._id = id
        self.email = email

    @property
    def id(self) -> int:
        return self._id

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        normalizado = self.normalizar_email(valor)
        if "@" not in normalizado:
            raise ValueError(f"email inválido: {valor!r}")
        self._email = normalizado

    @staticmethod
    def normalizar_email(texto: str) -> str:
        return texto.strip().lower()

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> "Usuario":
        return cls(datos["id"], datos["email"])
