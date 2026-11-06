import re
from collections import Counter, defaultdict


def group_by_initial(words: list[str]) -> dict[str, list[str]]:
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for w in words:
        if w:
            groups[w[0].lower()].append(w)
    return dict(groups)


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    return Counter(re.findall(r"\w+", text.lower())).most_common(n)


def invert_grouping(d: dict[str, int]) -> dict[int, list[str]]:
    inverse: defaultdict[int, list[str]] = defaultdict(list)
    for key, value in d.items():
        inverse[value].append(key)
    return dict(inverse)


def can_form(word: str, letters: str) -> bool:
    # What's missing (after subtracting what's available) must be empty.
    return not (Counter(word) - Counter(letters))
