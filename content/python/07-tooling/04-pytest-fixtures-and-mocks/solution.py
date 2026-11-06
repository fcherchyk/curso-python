"""Reference tests for weather.py."""

from unittest.mock import Mock

import pytest
from weather import BASE, save_report, summary, temperature


@pytest.fixture
def client():
    """Fake client: answers based on the city in the URL; "Atlantis" doesn't exist."""
    data = {"Boston": 21.456, "Denver": 18.04}

    def respond(url: str):
        city = url.rsplit("=", 1)[-1]
        if city not in data:
            raise KeyError(city)
        return {"temp_c": data[city]}

    return Mock(get_json=Mock(side_effect=respond))


def test_temperature_rounds(client):
    assert temperature("Boston", client) == 21.5


def test_temperature_requests_the_city_url():
    c = Mock()
    c.get_json.return_value = {"temp_c": 10}
    temperature("Denver", c)
    c.get_json.assert_called_once_with(f"{BASE}/current?city=Denver")


def test_summary_skips_failures(client):
    assert summary(["Boston", "Atlantis", "Denver"], client) == {"Boston": 21.5, "Denver": 18.0}


def test_save_report_sorted(tmp_path):
    path = tmp_path / "report.txt"
    save_report(path, {"Denver": 18.0, "Boston": 21.5})
    assert path.read_text(encoding="utf-8") == "Boston: 21.5\nDenver: 18.0\n"
