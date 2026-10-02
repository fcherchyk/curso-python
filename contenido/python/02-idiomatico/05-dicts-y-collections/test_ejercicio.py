from ejercicio import agrupar_por_inicial, invertir_agrupando, puede_formar, top_palabras


def test_agrupar_por_inicial():
    assert agrupar_por_inicial(["Ana", "auto", "", "Beto", "bote", "casa"]) == {
        "a": ["Ana", "auto"],
        "b": ["Beto", "bote"],
        "c": ["casa"],
    }


def test_agrupar_devuelve_dict_comun():
    assert type(agrupar_por_inicial(["x"])) is dict


def test_top_palabras():
    texto = "El perro y el gato. EL perro duerme; el gato no."
    assert top_palabras(texto, 3) == [("el", 4), ("perro", 2), ("gato", 2)]


def test_top_palabras_n_mayor_que_total():
    assert top_palabras("uno dos", 5) == [("uno", 1), ("dos", 1)]


def test_invertir_agrupando():
    assert invertir_agrupando({"ana": 9, "beto": 7, "caro": 9}) == {
        9: ["ana", "caro"],
        7: ["beto"],
    }
    assert type(invertir_agrupando({"a": 1})) is dict


def test_puede_formar():
    assert puede_formar("sol", "losa")
    assert puede_formar("", "abc")
    assert not puede_formar("oso", "sol")
    assert not puede_formar("Sol", "sol")
