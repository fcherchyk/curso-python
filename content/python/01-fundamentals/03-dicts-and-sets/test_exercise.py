from exercise import comunes, contar_caracteres, hay_duplicados, unicos_en_orden


def test_unicos_en_orden():
    assert unicos_en_orden(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]
    assert unicos_en_orden([]) == []


def test_comunes():
    assert comunes([3, 1, 2, 3], [3, 4, 1]) == [1, 3]
    assert comunes([1, 2], [3]) == []


def test_contar_caracteres():
    assert contar_caracteres("hola ola") == {"h": 1, "o": 2, "l": 2, "a": 2, " ": 1}
    assert list(contar_caracteres("ba")) == ["b", "a"], "tiene que respetar el orden"
    assert contar_caracteres("") == {}


def test_hay_duplicados():
    assert hay_duplicados([1, 2, 3, 1])
    assert not hay_duplicados([1, 2, 3])
    assert not hay_duplicados([])
