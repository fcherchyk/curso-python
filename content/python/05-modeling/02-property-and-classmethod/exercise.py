"""property, classmethod and staticmethod."""

from typing import Any

ABSOLUTE_ZERO = -273.15


class Temperature:
    """Temperature with two views: celsius and fahrenheit.

    - `celsius`: property with a setter; below absolute zero → ValueError
      (also when constructing).
    - `fahrenheit`: computed property WITH a setter (assigning it updates celsius).
    - `Temperature.from_fahrenheit(f)`: alternative constructor.
    """

    def __init__(self, celsius: float) -> None:
        raise NotImplementedError("TODO")

    # Implement: property celsius (+ setter), property fahrenheit (+ setter)
    # and the classmethod from_fahrenheit.


class User:
    """User with:

    - `id`: read-only (property without a setter).
    - `email`: property; on assignment it's normalized (strip + lowercase) and, if it has
      no "@", ValueError.
    - `User.normalize_email(text)`: staticmethod that does the normalization.
    - `User.from_dict({"id": 1, "email": "..."})`: classmethod.
    """

    def __init__(self, id: int, email: str) -> None:
        raise NotImplementedError("TODO")

    @staticmethod
    def normalize_email(text: str) -> str:
        raise NotImplementedError("TODO")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        raise NotImplementedError("TODO")
