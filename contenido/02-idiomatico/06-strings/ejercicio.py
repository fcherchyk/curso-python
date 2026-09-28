"""Strings idiomáticos."""

import re  # noqa: F401
from urllib.parse import urlencode  # noqa: F401


def formatear_pesos(monto: float) -> str:
    """Formateá en pesos con formato argentino: punto de miles y coma decimal.

    >>> formatear_pesos(1234.5)
    '$ 1.234,50'
    >>> formatear_pesos(-9876543.219)
    '$ -9.876.543,22'

    Pista: f-string con `,.2f` y después `str.maketrans` + `translate`.
    """
    raise NotImplementedError("TODO")


def slug(titulo: str) -> str:
    """Convertí un título en un slug para URLs: palabras en minúscula unidas con `-`.

    Una palabra es una secuencia de caracteres `\\w` (se mantienen los acentos).

    >>> slug("  ¡Hola, Mundo! Python 3.14  ")
    'hola-mundo-python-3-14'
    """
    raise NotImplementedError("TODO")


def parsear_opciones(texto: str) -> dict[str, str]:
    """Parseá `"clave=valor"` separados por `;`.

    - Sacá los espacios alrededor de claves y valores.
    - Ignorá los segmentos vacíos.
    - Si un segmento no tiene `=`, el valor es `""`.
    - El valor puede contener `=` (solo se parte por el primero).

    >>> parsear_opciones(" host = db.local ; debug ;; url=a=b ")
    {'host': 'db.local', 'debug': '', 'url': 'a=b'}
    """
    raise NotImplementedError("TODO")


def construir_url(host: str, *segmentos: str, https: bool = True, **query: str | int) -> str:
    """Construí una URL.

    - `segmentos` son partes del path.
    - `https` es keyword-only (ya está en la firma: va después de `*segmentos`).
    - `query` son parámetros del querystring, en el orden recibido.

    >>> construir_url("api.com", "v1", "users", page=2)
    'https://api.com/v1/users?page=2'
    >>> construir_url("api.com", https=False)
    'http://api.com/'

    Pista: `urllib.parse.urlencode`.
    """
    raise NotImplementedError("TODO")
