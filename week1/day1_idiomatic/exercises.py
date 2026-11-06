"""Day 1 — Idiomatic Python.

Complete each function by replacing the `raise NotImplementedError`.
Read `lesson.md` first and run the tests with:

    uv run pytest week1/day1_idiomatic
"""

import re
from collections import Counter, defaultdict
from urllib.parse import urlencode


def square_evens(nums: list[int]) -> list[int]:
    """Return the square of each even number, in the same order.

    Hint: a single list comprehension with `if`.

    >>> square_evens([1, 2, 3, 4])
    [4, 16]
    """
    return [(x*x) for x  in nums if x % 2 == 0]


def flatten(matrix: list[list[int]]) -> list[int]:
    """Flatten a list of lists (one level only).

    Hint: a nested comprehension; the order of the `for` clauses is the same
    as you would write with nested loops.

    >>> flatten([[1, 2], [3], []])
    [1, 2, 3]
    """
    return [x for row in matrix for x in row]

def invert_dict(d: dict[str, int]) -> dict[int, str]:
    """Swap keys and values (assume the values are unique).

    Hint: dict comprehension + `.items()`.

    >>> invert_dict({"a": 1, "b": 2})
    {1: 'a', 2: 'b'}
    """
    return {v:k for k,v in d.items()}


def group_by_initial(words: list[str]) -> dict[str, list[str]]:
    """Group words by their lowercase first letter, preserving order.

    Ignore empty strings.

    Hint: `collections.defaultdict(list)` or `dict.setdefault`.

    >>> group_by_initial(["Alice", "apple", "Bob"])
    {'a': ['Alice', 'apple'], 'b': ['Bob']}
    """
    return {letter.lower(): [w for w in words if w and w[0].lower() == letter.lower()] for letter in set(w[0] for w in words if w)}


def first_and_rest(seq: list[int]) -> tuple[int, list[int]]:
    """Return (first element, list with the rest).

    If the sequence is empty, raise ValueError.

    Hint: extended unpacking `a, *b = ...`.
    """
    return seq[0], seq[1:] if seq else ValueError("The sequence is empty")


def indices_of(seq: list[str], value: str) -> list[int]:
    """Indices where `value` appears.

    Hint: `enumerate`, never `range(len(...))`.

    >>> indices_of(["a", "b", "a"], "a")
    [0, 2]
    """
    raise NotImplementedError("TODO")


def pair_up(names: list[str], grades: list[float]) -> dict[str, float]:
    """Build a name -> grade dict.

    If the lists have different lengths, it must raise ValueError.

    Hint: `zip(..., strict=True)` (3.10+) already does that for you.
    """
    raise NotImplementedError("TODO")


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """The `n` most frequent words (lowercased) with their counts.

    A "word" is a sequence of `\\w` characters. On ties, the one that
    appeared first in the text wins.

    Hint: `re.findall` + `collections.Counter.most_common`.

    >>> top_words("Hello hello bye", 1)
    [('hello', 2)]
    """
    raise NotImplementedError("TODO")


def sort_people(people: list[dict[str, str | int]]) -> list[str]:
    """Return the names sorted by age descending and, for equal ages,
    by name ascending.

    Each person is `{"name": str, "age": int}`.

    Hint: `sorted(..., key=lambda p: (...))` with a tuple as the key.
    """
    raise NotImplementedError("TODO")


def build_url(host: str, *segments: str, https: bool = True, **query: str | int) -> str:
    """Build a URL.

    - `segments` are path parts (variable positional arguments).
    - `https` is keyword-only (it is already in the signature: it comes after `*segments`).
    - `query` are query string parameters, in the order received.

    >>> build_url("api.com", "v1", "users", page=2)
    'https://api.com/v1/users?page=2'
    >>> build_url("api.com", https=False)
    'http://api.com/'

    Hint: `urllib.parse.urlencode`.
    """
    raise NotImplementedError("TODO")


def merge_config(base: dict[str, object], *overrides: dict[str, object]) -> dict[str, object]:
    """Merge dictionaries: the ones on the right override the ones on the left.

    Don't modify `base`.

    Hint: the dict `|` operator (3.9+).
    """
    raise NotImplementedError("TODO")
