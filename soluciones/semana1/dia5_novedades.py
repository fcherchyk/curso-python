"""Día 5 — Novedades 3.8 a 3.14: match, walrus, ExceptionGroup, f-strings, tomllib.

    uv run pytest semana1/dia5_novedades
"""

import tomllib
from dataclasses import dataclass
from typing import IO, Any


@dataclass
class Circulo:
    radio: float


@dataclass
class Rectangulo:
    ancho: float
    alto: float


# ---------------------------------------------------------------------------
# match / case (3.10)
# ---------------------------------------------------------------------------


def interpretar_comando(comando: str) -> str:
    """Interpretá comandos de texto con `match` sobre `comando.split()`:

    - "salir" o "quit"          -> "chau"
    - "ir <dir>"                -> "yendo a <dir>"   (dir: norte/sur/este/oeste)
    - "ir <otra cosa>"          -> "dirección inválida"
    - "tomar <obj> [<obj>...]"  -> "tomaste: a, b"   (uno o más objetos)
    - ""                        -> "decí algo"
    - cualquier otra cosa       -> "no entiendo"

    Pista: patrones de secuencia, `|`, capturas con `*resto` y guardas `if`.
    """
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
    """Patrones de mapeo sobre eventos tipo JSON:

    - {"tipo": "click", "x": int, "y": int}   -> "click en (x, y)"
    - {"tipo": "tecla", "tecla": "enter"}     -> "confirmar"
    - {"tipo": "tecla", "tecla": str}         -> "tecla <tecla>"
    - {"tipo": "scroll", "delta": d} con d<0  -> "scroll abajo" / d>0 -> "scroll arriba"
    - otro                                    -> "desconocido"

    Las claves extra se ignoran (así funcionan los patrones de mapeo).
    Pista: `{"x": int(x)}` valida el tipo y captura a la vez.
    """
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
    """Patrones de clase:

    - Circulo de radio 0 o Rectangulo con algún lado 0 -> "degenerada"
    - Circulo(r)                                        -> "círculo de radio r"
    - Rectangulo(a, a) (lados iguales)                  -> "cuadrado de lado a"
    - Rectangulo(a, b)                                  -> "rectángulo a x b"
    - otra cosa                                         -> TypeError

    Pista: `case Circulo(radio=0)`, `case Rectangulo(ancho=a, alto=b) if a == b`.
    """
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


# ---------------------------------------------------------------------------
# Walrus := (3.8)
# ---------------------------------------------------------------------------


def leer_en_bloques(archivo: IO[str], tamanio: int) -> list[str]:
    """Leé el archivo en bloques de `tamanio` caracteres hasta el final.

    Pista: `while (bloque := archivo.read(tamanio)):`
    """
    bloques = []
    while bloque := archivo.read(tamanio):
        bloques.append(bloque)
    return bloques


def largos_mayores(palabras: list[str], minimo: int) -> list[int]:
    """Largos de las palabras con largo > minimo, calculando len() UNA vez
    por palabra.

    Pista: `[n for p in palabras if (n := len(p)) > minimo]`.
    """
    return [n for p in palabras if (n := len(p)) > minimo]


# ---------------------------------------------------------------------------
# ExceptionGroup y except* (3.11)
# ---------------------------------------------------------------------------


def validar_usuario(datos: dict[str, Any]) -> None:
    """Validá TODOS los campos y reportá todos los errores juntos.

    - "nombre": str no vacío                  -> si no, ValueError("nombre")
    - "edad": int                             -> si no es int, TypeError("edad")
    - "edad" >= 0                             -> si es negativa, ValueError("edad")
    - "email": contiene "@"                   -> si no, ValueError("email")

    Si hay errores, levantá `ExceptionGroup("usuario inválido", errores)`.
    Campos faltantes cuentan como inválidos.
    """
    errores: list[Exception] = []
    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre:
        errores.append(ValueError("nombre"))
    edad = datos.get("edad")
    if not isinstance(edad, int):
        errores.append(TypeError("edad"))
    elif edad < 0:
        errores.append(ValueError("edad"))
    if "@" not in str(datos.get("email", "")):
        errores.append(ValueError("email"))
    if errores:
        raise ExceptionGroup("usuario inválido", errores)


def clasificar_errores(datos: dict[str, Any]) -> dict[str, list[str]]:
    """Llamá a `validar_usuario` y clasificá los errores con `except*`.

    Devolvé {"valor": [...mensajes de ValueError], "tipo": [...de TypeError]}.
    Si no hay errores, ambas listas vacías.

    Pista: dentro de `except* ValueError as grupo:`, `grupo.exceptions` es
    la tupla con las ValueError.
    """
    resultado: dict[str, list[str]] = {"valor": [], "tipo": []}
    try:
        validar_usuario(datos)
    except* ValueError as grupo:
        resultado["valor"] = [str(e) for e in grupo.exceptions]
    except* TypeError as grupo:
        resultado["tipo"] = [str(e) for e in grupo.exceptions]
    return resultado


# ---------------------------------------------------------------------------
# f-strings con format spec
# ---------------------------------------------------------------------------


def tabla_precios(filas: list[tuple[str, float]]) -> str:
    """Formateá una tabla de ancho fijo, una línea por fila, unidas con "\\n":

    - nombre alineado a la izquierda en 12 caracteres
    - precio alineado a la derecha en 10, con separador de miles y 2 decimales
    - al final una línea "TOTAL" con el mismo formato

    >>> print(tabla_precios([("café", 1500.5)]))
    café          1,500.50
    TOTAL         1,500.50
    """
    lineas = [f"{nombre:<12}{precio:>10,.2f}" for nombre, precio in filas]
    total = sum(p for _, p in filas)
    lineas.append(f"{'TOTAL':<12}{total:>10,.2f}")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# tomllib (3.11) + operador | de dicts (3.9) + removeprefix (3.9)
# ---------------------------------------------------------------------------

DEFAULTS: dict[str, Any] = {"host": "localhost", "port": 8000, "debug": False}


def cargar_config(texto_toml: str) -> dict[str, Any]:
    """Parseá TOML y devolvé la sección [server] mezclada sobre DEFAULTS.

    Si no hay sección [server], devolvé una copia de DEFAULTS.
    Además, si "host" empieza con "http://" o "https://", quitá el prefijo.

    Pista: `tomllib.loads`, `DEFAULTS | seccion`, `str.removeprefix`.
    """
    seccion = tomllib.loads(texto_toml).get("server", {})
    config = DEFAULTS | seccion
    config["host"] = config["host"].removeprefix("https://").removeprefix("http://")
    return config
