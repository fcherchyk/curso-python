import re
from collections import Counter, defaultdict


def agrupar_por_inicial(palabras: list[str]) -> dict[str, list[str]]:
    grupos: defaultdict[str, list[str]] = defaultdict(list)
    for p in palabras:
        if p:
            grupos[p[0].lower()].append(p)
    return dict(grupos)


def top_palabras(texto: str, n: int) -> list[tuple[str, int]]:
    return Counter(re.findall(r"\w+", texto.lower())).most_common(n)


def invertir_agrupando(d: dict[str, int]) -> dict[int, list[str]]:
    inverso: defaultdict[int, list[str]] = defaultdict(list)
    for clave, valor in d.items():
        inverso[valor].append(clave)
    return dict(inverso)


def puede_formar(palabra: str, letras: str) -> bool:
    # Lo que falta (descontando lo disponible) tiene que estar vacío.
    return not (Counter(palabra) - Counter(letras))
