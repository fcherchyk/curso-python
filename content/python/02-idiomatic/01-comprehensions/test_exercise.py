from exercise import aplanar, dominios, invertir_dict, pares_al_cuadrado


def test_pares_al_cuadrado():
    assert pares_al_cuadrado([1, 2, 3, 4, 6]) == [4, 16, 36]


def test_pares_al_cuadrado_vacio():
    assert pares_al_cuadrado([]) == []
    assert pares_al_cuadrado([1, 3, 5]) == []


def test_aplanar():
    assert aplanar([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]


def test_invertir_dict():
    assert invertir_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert invertir_dict({}) == {}


def test_dominios():
    emails = ["ana@Gmail.com", "beto@gmail.com", "x@uba.ar", "sin-arroba"]
    assert dominios(emails) == {"gmail.com", "uba.ar"}


def test_dominios_devuelve_set():
    assert isinstance(dominios(["a@b.c"]), set)
