from itertools import pairwise


def indices_of(seq: list[str], value: str) -> list[int]:
    return [i for i, x in enumerate(seq) if x == value]


def pair_up(names: list[str], grades: list[float]) -> dict[str, float]:
    return dict(zip(names, grades, strict=True))


def differences(nums: list[int]) -> list[int]:
    return [b - a for a, b in pairwise(nums)]


def number_lines(lines: list[str], start: int = 1) -> list[str]:
    return [f"{n:>3} | {line}" for n, line in enumerate(lines, start=start)]
