def agregar_item(item: str, lista: list[str] | None = None) -> list[str]:
    if lista is None:
        lista = []
    lista.append(item)
    return lista


def promedio(*numeros: float) -> float:
    if not numeros:
        raise ValueError("hace falta al menos un número")
    return sum(numeros) / len(numeros)


def crear_usuario(nombre: str, /, *, admin: bool = False, **extra: object) -> dict[str, object]:
    return {"nombre": nombre, "admin": admin, **extra}


def formatear_atributos(**attrs: object) -> str:
    partes = []
    for nombre, valor in attrs.items():
        # `is True` / `is False`: el 0 es un valor válido, no un booleano.
        if valor is None or valor is False:
            continue
        partes.append(nombre if valor is True else f'{nombre}="{valor}"')
    return " ".join(partes)
