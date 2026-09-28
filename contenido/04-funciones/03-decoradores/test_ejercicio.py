import pytest
from ejercicio import MANEJADORES, contar_llamadas, despachar, manejador, memoizar


def test_contar_llamadas():
    @contar_llamadas
    def saludar(nombre):
        """Saluda."""
        return f"hola {nombre}"

    assert saludar.llamadas == 0
    assert saludar("ana") == "hola ana"
    saludar(nombre="beto")
    assert saludar.llamadas == 2
    assert saludar.__name__ == "saludar"
    assert saludar.__doc__ == "Saluda."


def test_memoizar():
    llamadas = []

    @memoizar
    def lento(a, b):
        llamadas.append((a, b))
        return a + b

    assert lento(1, 2) == 3
    assert lento(1, 2) == 3
    assert lento(2, 1) == 3
    assert llamadas == [(1, 2), (2, 1)]
    assert len(lento.cache) == 2
    assert lento.__name__ == "lento"


def test_memoizar_fibonacci_rapido():
    @memoizar
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(80) == 23416728348467685


def test_manejador_registra_sin_envolver():
    def al_iniciar(x):
        return x * 2

    decorada = manejador(al_iniciar)
    assert decorada is al_iniciar
    assert MANEJADORES["al_iniciar"] is al_iniciar


def test_despachar():
    @manejador
    def sumar(a, b):
        return a + b

    assert despachar("sumar", 2, 3) == 5


def test_despachar_inexistente():
    with pytest.raises(KeyError):
        despachar("no_existe")
