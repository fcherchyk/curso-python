import math
from dataclasses import asdict, dataclass, field, replace
from typing import Any


@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    def distance(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int = 0
    patch: int = 0

    @classmethod
    def from_str(cls, text: str) -> "Version":
        return cls(*(int(p) for p in text.split(".")))  # int() already raises ValueError

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class Order:
    customer: str
    items: list[str] = field(default_factory=list)
    status: str = "new"

    def __post_init__(self) -> None:
        if not self.customer.strip():
            raise ValueError("the order needs a customer")

    def with_status(self, new: str) -> "Order":
        return replace(self, status=new)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
