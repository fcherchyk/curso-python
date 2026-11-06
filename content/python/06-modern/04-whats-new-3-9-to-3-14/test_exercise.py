from exercise import DEFAULTS, load_config, price_table, time_in


def test_price_table():
    table = price_table([("coffee", 1500.5), ("croissants", 12.0)])
    assert table == "coffee        1,500.50\ncroissants       12.00\nTOTAL         1,512.50"


def test_load_config():
    toml = """
    [server]
    host = "https://api.example.com"
    port = 9000
    """
    assert load_config(toml) == {"host": "api.example.com", "port": 9000, "debug": False}


def test_load_config_without_section_does_not_mutate_defaults():
    config = load_config('title = "x"')
    assert config == DEFAULTS
    config["port"] = 1
    assert DEFAULTS["port"] == 8000


def test_time_in():
    assert time_in("2026-01-15T15:30:00Z", "America/Argentina/Buenos_Aires") == "12:30"
    assert time_in("2026-01-15T15:30:00+00:00", "Europe/Madrid") == "16:30"


def test_time_in_respects_daylight_saving_time():
    assert time_in("2026-07-15T15:30:00Z", "Europe/Madrid") == "17:30"
