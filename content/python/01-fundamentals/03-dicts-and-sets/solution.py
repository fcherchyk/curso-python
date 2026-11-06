def unique_in_order(xs: list[str]) -> list[str]:
    return list(dict.fromkeys(xs))


def common(a: list[int], b: list[int]) -> list[int]:
    return sorted(set(a) & set(b))


def count_chars(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for c in text:
        counts[c] = counts.get(c, 0) + 1
    return counts


def has_duplicates(xs: list[int]) -> bool:
    return len(set(xs)) != len(xs)
