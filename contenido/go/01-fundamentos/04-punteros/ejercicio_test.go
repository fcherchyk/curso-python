package ejercicio

import (
	"slices"
	"testing"
)

func TestIntercambiar(t *testing.T) {
	a, b := 1, 2
	Intercambiar(&a, &b)
	if a != 2 || b != 1 {
		t.Errorf("después de Intercambiar: a=%d b=%d, quiero a=2 b=1", a, b)
	}
}

func TestDepositar(t *testing.T) {
	c := Cuenta{Titular: "ana", Saldo: 10}
	Depositar(&c, 90)
	if c.Saldo != 100 {
		t.Errorf("Saldo = %d, quiero 100", c.Saldo)
	}
}

func TestNuevaCuenta(t *testing.T) {
	c := NuevaCuenta("beto")
	if c == nil {
		t.Fatal("NuevaCuenta devolvió nil")
	}
	if c.Titular != "beto" || c.Saldo != 0 {
		t.Errorf("NuevaCuenta = %+v, quiero {Titular:beto Saldo:0}", *c)
	}
	if NuevaCuenta("x") == NuevaCuenta("x") {
		t.Errorf("cada llamada tiene que crear una cuenta distinta")
	}
}

func TestBuscarDevuelvePunteroAlElemento(t *testing.T) {
	cuentas := []Cuenta{{"ana", 5}, {"beto", 7}, {"ana", 9}}
	c := Buscar(cuentas, "ana")
	if c == nil {
		t.Fatal(`Buscar(cuentas, "ana") devolvió nil`)
	}
	c.Saldo = 1000
	if cuentas[0].Saldo != 1000 {
		t.Errorf("el puntero tiene que apuntar al elemento del slice, no a una copia")
	}
	if Buscar(cuentas, "zoe") != nil {
		t.Errorf(`Buscar(cuentas, "zoe") tiene que devolver nil`)
	}
}

func TestDuplicarEnLugar(t *testing.T) {
	xs := []int{1, 2, 3}
	DuplicarEnLugar(xs)
	if !slices.Equal(xs, []int{2, 4, 6}) {
		t.Errorf("después de DuplicarEnLugar: %v, quiero [2 4 6]", xs)
	}
}
