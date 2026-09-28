import pytest

from semana1.dia1_idiomatico.ejercicios import (
    agrupar_por_inicial,
    aplanar,
    construir_url,
    emparejar,
    fusionar_config,
    indices_de,
    invertir_dict,
    ordenar_personas,
    pares_al_cuadrado,
    primero_y_resto,
    top_palabras,
)


def test_pares_al_cuadrado():
    assert pares_al_cuadrado([1, 2, 3, 4, 6]) == [4, 16, 36]
    assert pares_al_cuadrado([]) == []


def test_aplanar():
    assert aplanar([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]


def test_invertir_dict():
    assert invertir_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_agrupar_por_inicial():
    assert agrupar_por_inicial(["Ana", "auto", "", "Beto", "bote", "casa"]) == {
        "a": ["Ana", "auto"],
        "b": ["Beto", "bote"],
        "c": ["casa"],
    }


def test_agrupar_devuelve_dict_comun():
    # Un defaultdict "filtra" comportamiento raro hacia afuera: devolvé un dict.
    assert type(agrupar_por_inicial(["x"])) is dict


def test_primero_y_resto():
    assert primero_y_resto([1, 2, 3]) == (1, [2, 3])
    assert primero_y_resto([7]) == (7, [])
    with pytest.raises(ValueError):
        primero_y_resto([])


def test_indices_de():
    assert indices_de(["a", "b", "a", "c", "a"], "a") == [0, 2, 4]
    assert indices_de(["a"], "z") == []


def test_emparejar():
    assert emparejar(["ana", "beto"], [9.5, 7]) == {"ana": 9.5, "beto": 7}
    with pytest.raises(ValueError):
        emparejar(["ana"], [1, 2])


def test_top_palabras():
    texto = "El perro y el gato. EL perro duerme; el gato no."
    assert top_palabras(texto, 3) == [("el", 4), ("perro", 2), ("gato", 2)]


def test_ordenar_personas():
    personas = [
        {"nombre": "Zoe", "edad": 30},
        {"nombre": "Ana", "edad": 25},
        {"nombre": "Beto", "edad": 30},
    ]
    assert ordenar_personas(personas) == ["Beto", "Zoe", "Ana"]


def test_construir_url():
    assert construir_url("api.com", "v1", "users", page=2, q="x y") == (
        "https://api.com/v1/users?page=2&q=x+y"
    )
    assert construir_url("api.com", https=False) == "http://api.com/"


def test_construir_url_https_es_keyword_only():
    # "False" como posicional se toma como un segmento más, no como https.
    assert construir_url("a.com", "b", "c").startswith("https://")


def test_fusionar_config():
    base = {"debug": False, "port": 80}
    res = fusionar_config(base, {"port": 8080}, {"debug": True, "host": "x"})
    assert res == {"debug": True, "port": 8080, "host": "x"}
    assert base == {"debug": False, "port": 80}, "no hay que mutar base"
