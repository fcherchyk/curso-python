"""Excepciones."""

from pathlib import Path


def a_entero(texto: str, default: int | None = None) -> int | None:
    """Convertí `texto` a int (se permiten espacios alrededor). Si no se puede,
    devolvé `default`. Usá EAFP (try/except), no `isdigit`.

    >>> a_entero(" 42 ")
    42
    >>> a_entero("4.2", default=-1)
    -1
    """
    raise NotImplementedError("TODO")


class SaldoInsuficiente(Exception):
    """Completá: guardá `saldo` y `monto` como atributos y armá un mensaje
    que incluya los dos valores."""

    def __init__(self, saldo: float, monto: float) -> None:
        raise NotImplementedError("TODO")


def retirar(saldo: float, monto: float) -> float:
    """Devolvé el saldo después de retirar `monto`.

    - monto <= 0 → ValueError
    - monto > saldo → SaldoInsuficiente(saldo, monto)
    """
    raise NotImplementedError("TODO")


class ConfigError(Exception):
    pass


def leer_config(ruta: Path) -> dict[str, str]:
    """Leé un archivo de líneas `clave=valor` (ignorá las vacías) y devolvé un dict.

    Si el archivo no existe, levantá ConfigError encadenando el FileNotFoundError
    original (`raise ... from e`).
    """
    raise NotImplementedError("TODO")


def procesar_todos(textos: list[str]) -> tuple[list[int], list[str]]:
    """Convertí cada texto a int. No cortes en el primer error: devolvé
    (números convertidos, textos que fallaron), en orden.

    >>> procesar_todos(["1", "x", "3"])
    ([1, 3], ['x'])
    """
    raise NotImplementedError("TODO")
