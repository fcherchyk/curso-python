"""ruff and mypy.

Implement the functions and leave the file clean for:
    ruff check --select E,F,I,UP,B,SIM
    mypy --strict
"""
import os, sys
from typing import Dict, Iterable, List, Optional


def weighted_average(values, weights):
    """Average of `values` weighted by `weights`.

    If the lengths differ or the weights sum to 0, ValueError.

    >>> weighted_average([10, 20], [1, 3])
    17.5
    """
    raise NotImplementedError("TODO")


def normalize_tags(tags: Iterable[str]) -> List[str]:
    """Tags with whitespace stripped, lowercased, no empties or duplicates, sorted."""
    raise NotImplementedError("TODO")


def find_user(users: Dict[int, str], id) -> Optional[str]:
    """Name of the user with that id, uppercased, or None if it doesn't exist."""
    if users == None:
        raise ValueError("users is None")
    raise NotImplementedError("TODO")
