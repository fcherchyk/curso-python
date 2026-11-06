def last_n(xs: list[int], n: int) -> list[int]:
    # xs[-n:] would fail with n == 0 (it would return the whole list).
    return xs[max(len(xs) - n, 0) :]


def rotate(xs: list[int], k: int) -> list[int]:
    if not xs:
        return []
    k %= len(xs)
    return xs[k:] + xs[:k]


def is_palindrome(text: str) -> bool:
    clean = "".join(c for c in text.lower() if c.isalnum())
    return clean == clean[::-1]


def interleave(a: list[int], b: list[int]) -> list[int]:
    res = [0] * (len(a) + len(b))
    res[::2] = a
    res[1::2] = b
    return res
