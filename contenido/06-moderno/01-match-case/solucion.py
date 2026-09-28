from dataclasses import dataclass
from typing import Any


@dataclass
class Circulo:
    radio: float


@dataclass
class Rectangulo:
    ancho: float
    alto: float


def interpretar_comando(comando: str) -> str:
    match comando.split():
        case []:
            return "decí algo"
        case ["salir" | "quit"]:
            return "chau"
        case ["ir", ("norte" | "sur" | "este" | "oeste") as direccion]:
            return f"yendo a {direccion}"
        case ["ir", _]:
            return "dirección inválida"
        case ["tomar", *objetos] if objetos:
            return "tomaste: " + ", ".join(objetos)
        case _:
            return "no entiendo"


def procesar_evento(evento: dict[str, Any]) -> str:
    match evento:
        case {"tipo": "click", "x": int(x), "y": int(y)}:
            return f"click en ({x}, {y})"
        case {"tipo": "tecla", "tecla": "enter"}:
            return "confirmar"
        case {"tipo": "tecla", "tecla": str(tecla)}:
            return f"tecla {tecla}"
        case {"tipo": "scroll", "delta": d} if d < 0:
            return "scroll abajo"
        case {"tipo": "scroll", "delta": d} if d > 0:
            return "scroll arriba"
        case _:
            return "desconocido"


def describir_figura(figura: object) -> str:
    match figura:
        case Circulo(radio=0) | Rectangulo(ancho=0) | Rectangulo(alto=0):
            return "degenerada"
        case Circulo(radio=r):
            return f"círculo de radio {r}"
        case Rectangulo(ancho=a, alto=b) if a == b:
            return f"cuadrado de lado {a}"
        case Rectangulo(ancho=a, alto=b):
            return f"rectángulo {a} x {b}"
        case _:
            raise TypeError(f"figura desconocida: {figura!r}")
