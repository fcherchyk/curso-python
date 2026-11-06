"""Idiomatic strings."""

import re  # noqa: F401
from urllib.parse import urlencode  # noqa: F401


def format_pesos(amount: float) -> str:
    """Format as Argentine pesos: dot as the thousands separator and comma for decimals.

    >>> format_pesos(1234.5)
    '$ 1.234,50'
    >>> format_pesos(-9876543.219)
    '$ -9.876.543,22'

    Hint: f-string with `,.2f`, then `str.maketrans` + `translate`.
    """
    raise NotImplementedError("TODO")


def slug(title: str) -> str:
    """Turn a title into a URL slug: lowercase words joined with `-`.

    A word is a sequence of `\\w` characters (accented letters are kept).

    >>> slug("  Hello, World! Python 3.14  ")
    'hello-world-python-3-14'
    """
    raise NotImplementedError("TODO")


def parse_options(text: str) -> dict[str, str]:
    """Parse `"key=value"` pairs separated by `;`.

    - Strip the whitespace around keys and values.
    - Ignore empty segments.
    - If a segment has no `=`, the value is `""`.
    - The value may contain `=` (split only on the first one).

    >>> parse_options(" host = db.local ; debug ;; url=a=b ")
    {'host': 'db.local', 'debug': '', 'url': 'a=b'}
    """
    raise NotImplementedError("TODO")


def build_url(host: str, *segments: str, https: bool = True, **query: str | int) -> str:
    """Build a URL.

    - `segments` are parts of the path.
    - `https` is keyword-only (already in the signature: it comes after `*segments`).
    - `query` are querystring parameters, in the order received.

    >>> build_url("api.com", "v1", "users", page=2)
    'https://api.com/v1/users?page=2'
    >>> build_url("api.com", https=False)
    'http://api.com/'

    Hint: `urllib.parse.urlencode`.
    """
    raise NotImplementedError("TODO")
