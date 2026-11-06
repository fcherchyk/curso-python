def unicos_en_orden(xs: list[str]) -> list[str]:
    return list(dict.fromkeys(xs))


def comunes(a: list[int], b: list[int]) -> list[int]:
    return sorted(set(a) & set(b))


def contar_caracteres(texto: str) -> dict[str, int]:
    conteo: dict[str, int] = {}
    for c in texto:
        conteo[c] = conteo.get(c, 0) + 1
    return conteo


def hay_duplicados(xs: list[int]) -> bool:
    return len(set(xs)) != len(xs)
