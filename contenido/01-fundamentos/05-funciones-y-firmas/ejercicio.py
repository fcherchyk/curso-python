"""Funciones y firmas.

En algunos ejercicios también tenés que escribir la FIRMA (fijate los tests).
"""


def agregar_item(item: str, lista: list[str] | None = None) -> list[str]:
    """Agregá `item` a `lista` y devolvela. Si no te pasan lista, empezá una nueva
    en CADA llamada (sin el bug del default mutable).

    >>> agregar_item("a")
    ['a']
    >>> agregar_item("b")
    ['b']
    """
    raise NotImplementedError("TODO")


def promedio(*numeros: float) -> float:
    """Promedio de una cantidad variable de números. Sin números, ValueError.

    >>> promedio(1, 2, 3, 4)
    2.5
    """
    raise NotImplementedError("TODO")


def crear_usuario(nombre, admin=False, **extra):  # ← corregí esta firma
    """Devolvé un dict con nombre, admin y los datos extra.

    La firma tiene que ser:
    - `nombre`: SOLO posicional.
    - `admin`: SOLO keyword, por defecto False.
    - cualquier otro dato por keyword va a `extra`.

    >>> crear_usuario("ana", admin=True, email="a@b.c")
    {'nombre': 'ana', 'admin': True, 'email': 'a@b.c'}
    """
    raise NotImplementedError("TODO")


def formatear_atributos(**attrs: object) -> str:
    """Convertí los keyword arguments en atributos HTML, en el orden recibido.

    Los que valen `True` van solo con el nombre; los que valen False o None se omiten.

    >>> formatear_atributos(id="x", disabled=True, hidden=False, title="Hola")
    'id="x" disabled title="Hola"'
    """
    raise NotImplementedError("TODO")
