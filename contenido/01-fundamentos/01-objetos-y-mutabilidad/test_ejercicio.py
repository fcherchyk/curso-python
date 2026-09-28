from decimal import Decimal

from ejercicio import agregar_sin_mutar, copiar_matriz, repartir, sumar_precios


def test_agregar_sin_mutar():
    xs = [1, 2]
    res = agregar_sin_mutar(xs, 3)
    assert res == [1, 2, 3]
    assert xs == [1, 2], "no hay que mutar la lista original"
    assert res is not xs


def test_copiar_matriz_es_independiente():
    m = [[1, 2], [3, 4]]
    c = copiar_matriz(m)
    assert c == m
    c[0].append(99)
    c.append([5])
    assert m == [[1, 2], [3, 4]], "modificar la copia cambió el original"


def test_sumar_precios_exacto():
    assert sumar_precios(["0.10", "0.20"]) == Decimal("0.30")
    assert sumar_precios(["19.99"] * 3) == Decimal("59.97")
    assert isinstance(sumar_precios(["1"]), Decimal)


def test_sumar_precios_vacio():
    assert sumar_precios([]) == 0


def test_repartir():
    assert repartir(17, 5) == (3, 2)
    assert repartir(10, 5) == (2, 0)


def test_repartir_negativo_cumple_la_identidad():
    cada, sobra = repartir(-7, 2)
    assert cada * 2 + sobra == -7
    assert (cada, sobra) == (-4, 1)
