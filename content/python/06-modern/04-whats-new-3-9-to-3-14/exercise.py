"""What's new from 3.9 to 3.14."""

import tomllib  # noqa: F401
from datetime import datetime  # noqa: F401
from typing import Any
from zoneinfo import ZoneInfo  # noqa: F401

DEFAULTS: dict[str, Any] = {"host": "localhost", "port": 8000, "debug": False}


def price_table(rows: list[tuple[str, float]]) -> str:
    """Fixed-width table, one line per row, joined with "\\n":

    - name left-aligned in 12 characters
    - price right-aligned in 10, with a thousands separator and 2 decimals
    - at the end, a "TOTAL" line with the same format

    >>> print(price_table([("coffee", 1500.5)]))
    coffee        1,500.50
    TOTAL         1,500.50
    """
    raise NotImplementedError("TODO")


def load_config(toml_text: str) -> dict[str, Any]:
    """Parse the TOML and return the [server] section merged over DEFAULTS
    (without mutating DEFAULTS). If there's no [server] section, a copy of DEFAULTS.

    Also, if "host" starts with "http://" or "https://", strip the prefix.
    """
    raise NotImplementedError("TODO")


def time_in(iso_moment: str, zone: str) -> str:
    """Convert an ISO 8601 moment with a zone (for example "2026-01-15T15:30:00Z") to the
    given IANA zone and return the local time as "HH:MM".

    >>> time_in("2026-01-15T15:30:00Z", "America/Argentina/Buenos_Aires")
    '12:30'
    """
    raise NotImplementedError("TODO")
