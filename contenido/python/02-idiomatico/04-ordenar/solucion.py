from operator import itemgetter


def ordenar_personas(personas: list[dict[str, str | int]]) -> list[str]:
    ordenadas = sorted(personas, key=lambda p: (-int(p["edad"]), str(p["nombre"])))
    return [str(p["nombre"]) for p in ordenadas]


def mas_caro(productos: list[dict[str, str | float]]) -> str | None:
    if not productos:
        return None
    # max devuelve el primero entre los empatados.
    return str(max(productos, key=itemgetter("precio"))["nombre"])


def ordenar_sin_mayusculas(palabras: list[str]) -> list[str]:
    return sorted(palabras, key=str.lower)


def ordenar_por(filas: list[dict[str, str]], *campos: str) -> list[dict[str, str]]:
    if not campos:
        return list(filas)
    return sorted(filas, key=itemgetter(*campos))
