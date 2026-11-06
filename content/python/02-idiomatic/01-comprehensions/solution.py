def squares_of_evens(nums: list[int]) -> list[int]:
    return [n * n for n in nums if n % 2 == 0]


def flatten(matrix: list[list[int]]) -> list[int]:
    return [x for row in matrix for x in row]


def invert_dict(d: dict[str, int]) -> dict[int, str]:
    return {v: k for k, v in d.items()}


def domains(emails: list[str]) -> set[str]:
    # partition doesn't fail when there is no "@": it returns an empty separator.
    return {e.partition("@")[2].lower() for e in emails if "@" in e}
