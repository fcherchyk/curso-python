from exercise import mas_caro, ordenar_personas, ordenar_por, ordenar_sin_mayusculas


def test_ordenar_personas():
    personas = [
        {"nombre": "Zoe", "edad": 30},
        {"nombre": "Ana", "edad": 25},
        {"nombre": "Beto", "edad": 30},
    ]
    assert ordenar_personas(personas) == ["Beto", "Zoe", "Ana"]


def test_ordenar_personas_no_muta():
    personas = [{"nombre": "B", "edad": 1}, {"nombre": "A", "edad": 2}]
    ordenar_personas(personas)
    assert personas[0]["nombre"] == "B"


def test_mas_caro():
    productos = [
        {"nombre": "pan", "precio": 1.2},
        {"nombre": "café", "precio": 9.8},
        {"nombre": "té", "precio": 9.8},
    ]
    assert mas_caro(productos) == "café"


def test_mas_caro_vacio():
    assert mas_caro([]) is None


def test_ordenar_sin_mayusculas():
    assert ordenar_sin_mayusculas(["banana", "Ana", "Cereza", "ana"]) == [
        "Ana",
        "ana",
        "banana",
        "Cereza",
    ]


def test_ordenar_por_varios_campos():
    filas = [
        {"pais": "UY", "ciudad": "Salto"},
        {"pais": "AR", "ciudad": "Rosario"},
        {"pais": "AR", "ciudad": "Córdoba"},
    ]
    res = ordenar_por(filas, "pais", "ciudad")
    assert [f["ciudad"] for f in res] == ["Córdoba", "Rosario", "Salto"]


def test_ordenar_por_sin_campos():
    filas = [{"a": "2"}, {"a": "1"}]
    res = ordenar_por(filas)
    assert res == filas
    assert res is not filas
