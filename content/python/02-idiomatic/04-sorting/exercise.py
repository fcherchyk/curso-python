"""Sorting.

Use `sorted`, `max` and `operator.itemgetter` with the `key` parameter.
"""

from operator import itemgetter  # noqa: F401  (it will come in handy)


def sort_people(people: list[dict[str, str | int]]) -> list[str]:
    """Return the names sorted by age descending and, for equal ages,
    by name ascending.

    Each person is `{"name": str, "age": int}`.

    >>> sort_people([{"name": "Zoe", "age": 30}, {"name": "Alice", "age": 25},
    ...              {"name": "Bob", "age": 30}])
    ['Bob', 'Zoe', 'Alice']
    """
    raise NotImplementedError("TODO")


def most_expensive(products: list[dict[str, str | float]]) -> str | None:
    """Name of the product with the highest `price`, or None if the list is empty.

    On ties, the first one that appears.

    >>> most_expensive([{"name": "bread", "price": 1.2}, {"name": "coffee", "price": 9.8}])
    'coffee'
    """
    raise NotImplementedError("TODO")


def sort_case_insensitive(words: list[str]) -> list[str]:
    """Sort alphabetically, ignoring uppercase vs. lowercase.

    Return the words exactly as they came in (don't lowercase them).

    >>> sort_case_insensitive(["banana", "Apple", "Cherry"])
    ['Apple', 'banana', 'Cherry']
    """
    raise NotImplementedError("TODO")


def sort_by(rows: list[dict[str, str]], *fields: str) -> list[dict[str, str]]:
    """Sort the rows by the given fields, in that order of priority.

    With no fields, return a copy without changing the order.

    >>> rows = [{"country": "CA", "city": "Toronto"}, {"country": "CA", "city": "Calgary"}]
    >>> [r["city"] for r in sort_by(rows, "country", "city")]
    ['Calgary', 'Toronto']
    """
    raise NotImplementedError("TODO")
