"""Dicts, defaultdict and Counter."""

import re  # noqa: F401
from collections import Counter, defaultdict  # noqa: F401


def group_by_initial(words: list[str]) -> dict[str, list[str]]:
    """Group words by their first letter in lowercase, keeping the order.

    Ignore empty strings. Return a plain `dict` (not a defaultdict).

    >>> group_by_initial(["Alice", "apple", "Bob"])
    {'a': ['Alice', 'apple'], 'b': ['Bob']}
    """
    raise NotImplementedError("TODO")


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """The `n` most frequent words (lowercased) with their counts.

    A "word" is a sequence of `\\w` characters. On ties, the one that
    appeared first in the text wins.

    Hint: `re.findall` + `Counter.most_common`.

    >>> top_words("Hello hello bye", 1)
    [('hello', 2)]
    """
    raise NotImplementedError("TODO")


def invert_grouping(d: dict[str, int]) -> dict[int, list[str]]:
    """Invert the dict: each value becomes a key, mapped to the list of original keys.

    >>> invert_grouping({"alice": 9, "bob": 7, "carol": 9})
    {9: ['alice', 'carol'], 7: ['bob']}
    """
    raise NotImplementedError("TODO")


def can_form(word: str, letters: str) -> bool:
    """Can you spell `word` using each letter in `letters` at most once?

    Treat uppercase and lowercase as different, exactly as given.

    Hint: `Counter` subtraction.

    >>> can_form("tea", "east")
    True
    >>> can_form("tee", "tea")
    False
    """
    raise NotImplementedError("TODO")
