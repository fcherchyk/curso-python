from exercise import DEFAULTS, cargar_config, hora_en, tabla_precios


def test_tabla_precios():
    tabla = tabla_precios([("café", 1500.5), ("medialunas", 12.0)])
    assert tabla == "café          1,500.50\nmedialunas       12.00\nTOTAL         1,512.50"


def test_cargar_config():
    toml = """
    [server]
    host = "https://api.ejemplo.com"
    port = 9000
    """
    assert cargar_config(toml) == {"host": "api.ejemplo.com", "port": 9000, "debug": False}


def test_cargar_config_sin_seccion_no_muta_defaults():
    config = cargar_config('titulo = "x"')
    assert config == DEFAULTS
    config["port"] = 1
    assert DEFAULTS["port"] == 8000


def test_hora_en():
    assert hora_en("2026-01-15T15:30:00Z", "America/Argentina/Buenos_Aires") == "12:30"
    assert hora_en("2026-01-15T15:30:00+00:00", "Europe/Madrid") == "16:30"


def test_hora_en_respeta_horario_de_verano():
    assert hora_en("2026-07-15T15:30:00Z", "Europe/Madrid") == "17:30"
