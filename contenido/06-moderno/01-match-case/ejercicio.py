"""Pattern matching: match / case.

Resolvé las tres funciones con `match` (nada de cadenas de if/elif).
"""

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
    """Interpretá comandos de texto con `match` sobre `comando.split()`:

    - "salir" o "quit"          -> "chau"
    - "ir <dir>"                -> "yendo a <dir>"   (dir: norte/sur/este/oeste)
    - "ir <otra cosa>"          -> "dirección inválida"
    - "tomar <obj> [<obj>...]"  -> "tomaste: a, b"   (uno o más objetos)
    - ""                        -> "decí algo"
    - cualquier otra cosa       -> "no entiendo"
    """
    raise NotImplementedError("TODO")


def procesar_evento(evento: dict[str, Any]) -> str:
    """Patrones de mapeo sobre eventos tipo JSON:

    - {"tipo": "click", "x": int, "y": int}   -> "click en (x, y)"
    - {"tipo": "tecla", "tecla": "enter"}     -> "confirmar"
    - {"tipo": "tecla", "tecla": str}         -> "tecla <tecla>"
    - {"tipo": "scroll", "delta": d} con d<0  -> "scroll abajo" / d>0 -> "scroll arriba"
    - otro                                    -> "desconocido"
    """
    raise NotImplementedError("TODO")


def describir_figura(figura: object) -> str:
    """Patrones de clase:

    - Circulo de radio 0 o Rectangulo con algún lado 0 -> "degenerada"
    - Circulo(r)                                        -> "círculo de radio r"
    - Rectangulo(a, a) (lados iguales)                  -> "cuadrado de lado a"
    - Rectangulo(a, b)                                  -> "rectángulo a x b"
    - otra cosa                                         -> TypeError
    """
    raise NotImplementedError("TODO")
