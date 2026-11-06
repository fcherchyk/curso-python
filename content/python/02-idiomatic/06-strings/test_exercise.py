from exercise import build_url, format_pesos, parse_options, slug


def test_format_pesos():
    assert format_pesos(1234.5) == "$ 1.234,50"
    assert format_pesos(0) == "$ 0,00"
    assert format_pesos(1_000_000) == "$ 1.000.000,00"


def test_format_pesos_negative_and_rounding():
    assert format_pesos(-9876543.219) == "$ -9.876.543,22"


def test_slug():
    assert slug("  Hello, World! Python 3.14  ") == "hello-world-python-3-14"
    assert slug("Café  au   LAIT") == "café-au-lait"
    assert slug("!!!") == ""


def test_parse_options():
    assert parse_options(" host = db.local ; debug ;; url=a=b ") == {
        "host": "db.local",
        "debug": "",
        "url": "a=b",
    }
    assert parse_options("") == {}


def test_build_url():
    assert build_url("api.com", "v1", "users", page=2, q="x y") == (
        "https://api.com/v1/users?page=2&q=x+y"
    )
    assert build_url("api.com", https=False) == "http://api.com/"


def test_build_url_segments_without_query():
    assert build_url("a.com", "b", "c") == "https://a.com/b/c"
