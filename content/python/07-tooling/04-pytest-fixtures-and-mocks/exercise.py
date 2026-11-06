"""Write TESTS for weather.py (the code is in the lesson).

Requirements:
- at least 4 test functions
- at least one fixture of your own (`@pytest.fixture`)
- use `Mock` (from unittest.mock) and the `tmp_path` fixture
- they must pass with the correct code and catch all 4 mutants
"""

from unittest.mock import Mock  # noqa: F401

import pytest  # noqa: F401
from weather import BASE, save_report, summary, temperature  # noqa: F401


def test_temperature():
    raise NotImplementedError("TODO: write the test")
