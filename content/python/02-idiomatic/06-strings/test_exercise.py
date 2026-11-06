from exercise import construir_url, formatear_pesos, parsear_opciones, slug


def test_formatear_pesos():
    assert formatear_pesos(1234.5) == "$ 1.234,50"
    assert formatear_pesos(0) == "$ 0,00"
    assert formatear_pesos(1_000_000) == "$ 1.000.000,00"


def test_formatear_pesos_negativo_y_redondeo():
    assert formatear_pesos(-9876543.219) == "$ -9.876.543,22"


def test_slug():
    assert slug("  ¡Hola, Mundo! Python 3.14  ") == "hola-mundo-python-3-14"
    assert slug("Canción  de   CUNA") == "canción-de-cuna"
    assert slug("!!!") == ""


def test_parsear_opciones():
    assert parsear_opciones(" host = db.local ; debug ;; url=a=b ") == {
        "host": "db.local",
        "debug": "",
        "url": "a=b",
    }
    assert parsear_opciones("") == {}


def test_construir_url():
    assert construir_url("api.com", "v1", "users", page=2, q="x y") == (
        "https://api.com/v1/users?page=2&q=x+y"
    )
    assert construir_url("api.com", https=False) == "http://api.com/"


def test_construir_url_segmentos_sin_query():
    assert construir_url("a.com", "b", "c") == "https://a.com/b/c"
