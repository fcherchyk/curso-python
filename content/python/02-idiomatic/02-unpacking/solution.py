def first_and_rest(seq: list[int]) -> tuple[int, list[int]]:
    if not seq:
        raise ValueError("empty sequence")
    first, *rest = seq
    return first, rest


def ends(seq: list[int]) -> tuple[int, int]:
    if not seq:
        raise ValueError("empty sequence")
    # With a single element, both patterns take that same value.
    first, *_ = seq
    *_, last = seq
    return first, last


def sum_points(points: list[tuple[int, int]]) -> tuple[int, int]:
    sx = sy = 0
    for x, y in points:
        sx += x
        sy += y
    return sx, sy


def merge_config(base: dict[str, object], *overrides: dict[str, object]) -> dict[str, object]:
    result = dict(base)
    for o in overrides:
        result |= o
    return result
