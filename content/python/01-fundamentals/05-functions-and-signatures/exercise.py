"""Functions and signatures.

In some exercises you also have to write the SIGNATURE (check the tests).
"""


def add_item(item: str, items: list[str] | None = None) -> list[str]:
    """Append `item` to `items` and return it. If no list is passed, start a new one
    on EVERY call (without the mutable default bug).

    >>> add_item("a")
    ['a']
    >>> add_item("b")
    ['b']
    """
    raise NotImplementedError("TODO")


def average(*numbers: float) -> float:
    """Average of a variable number of numbers. With no numbers, ValueError.

    >>> average(1, 2, 3, 4)
    2.5
    """
    raise NotImplementedError("TODO")


def create_user(name, admin=False, **extra):  # ← fix this signature
    """Return a dict with name, admin and the extra data.

    The signature must be:
    - `name`: positional-ONLY.
    - `admin`: keyword-ONLY, defaults to False.
    - any other keyword data goes into `extra`.

    >>> create_user("alice", admin=True, email="a@b.c")
    {'name': 'alice', 'admin': True, 'email': 'a@b.c'}
    """
    raise NotImplementedError("TODO")


def format_attributes(**attrs: object) -> str:
    """Turn the keyword arguments into HTML attributes, in the order received.

    Those set to `True` get just the name; those set to False or None are omitted.

    >>> format_attributes(id="x", disabled=True, hidden=False, title="Hello")
    'id="x" disabled title="Hello"'
    """
    raise NotImplementedError("TODO")
