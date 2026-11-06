from typing import Any

ABSOLUTE_ZERO = -273.15


class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius  # goes through the setter: validates on construction

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < ABSOLUTE_ZERO:
            raise ValueError(f"below absolute zero: {value}")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        return cls((f - 32) * 5 / 9)


class User:
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
    def email(self, value: str) -> None:
        normalized = self.normalize_email(value)
        if "@" not in normalized:
            raise ValueError(f"invalid email: {value!r}")
        self._email = normalized

    @staticmethod
    def normalize_email(text: str) -> str:
        return text.strip().lower()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(data["id"], data["email"])
