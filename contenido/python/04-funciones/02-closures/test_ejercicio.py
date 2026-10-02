from ejercicio import crear_contador, crear_limitador, crear_promediador, multiplicadores


def test_crear_contador_independientes():
    a, b = crear_contador(), crear_contador(10)
    assert [a(), a(), a()] == [0, 1, 2]
    assert [b(), b()] == [10, 11]
    assert a() == 3


def test_contador_es_closure():
    c = crear_contador()
    assert c.__closure__, "tiene que ser una closure (función interna)"


def test_multiplicadores():
    fs = multiplicadores(4)
    assert len(fs) == 4
    assert [f(10) for f in fs] == [0, 10, 20, 30]
    assert multiplicadores(0) == []


def test_crear_promediador():
    p = crear_promediador()
    assert p(10) == 10.0
    assert p(20) == 15.0
    assert p(60) == 30.0


def test_promediadores_independientes():
    p1, p2 = crear_promediador(), crear_promediador()
    p1(100)
    assert p2(1) == 1.0


def test_crear_limitador():
    puede = crear_limitador(2)
    assert [puede(), puede(), puede(), puede()] == [True, True, False, False]
    assert crear_limitador(0)() is False
