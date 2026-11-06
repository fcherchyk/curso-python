import math
from dataclasses import asdict, dataclass, field, replace
from typing import Any


@dataclass(frozen=True, slots=True)
class Punto:
    x: float
    y: float

    def distancia(self, otro: "Punto") -> float:
        return math.hypot(self.x - otro.x, self.y - otro.y)

    def __add__(self, otro: "Punto") -> "Punto":
        return Punto(self.x + otro.x, self.y + otro.y)


@dataclass(frozen=True, order=True)
class Version:
    mayor: int
    menor: int = 0
    parche: int = 0

    @classmethod
    def desde_str(cls, texto: str) -> "Version":
        return cls(*(int(p) for p in texto.split(".")))  # int() ya levanta ValueError

    def __str__(self) -> str:
        return f"{self.mayor}.{self.menor}.{self.parche}"


@dataclass
class Pedido:
    cliente: str
    items: list[str] = field(default_factory=list)
    estado: str = "nuevo"

    def __post_init__(self) -> None:
        if not self.cliente.strip():
            raise ValueError("el pedido necesita un cliente")

    def con_estado(self, nuevo: str) -> "Pedido":
        return replace(self, estado=nuevo)

    def a_dict(self) -> dict[str, Any]:
        return asdict(self)
