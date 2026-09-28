def ultimos(xs: list[int], n: int) -> list[int]:
    # xs[-n:] fallaría con n == 0 (devolvería toda la lista).
    return xs[max(len(xs) - n, 0) :]


def rotar(xs: list[int], k: int) -> list[int]:
    if not xs:
        return []
    k %= len(xs)
    return xs[k:] + xs[:k]


def es_palindromo(texto: str) -> bool:
    limpio = "".join(c for c in texto.lower() if c.isalnum())
    return limpio == limpio[::-1]


def intercalar(a: list[int], b: list[int]) -> list[int]:
    res = [0] * (len(a) + len(b))
    res[::2] = a
    res[1::2] = b
    return res
