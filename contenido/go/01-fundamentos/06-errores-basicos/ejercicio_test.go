package ejercicio

import (
	"errors"
	"slices"
	"strconv"
	"strings"
	"testing"
)

func TestDividir(t *testing.T) {
	if got, err := Dividir(10, 4); err != nil || got != 2.5 {
		t.Errorf("Dividir(10, 4) = (%v, %v), quiero (2.5, nil)", got, err)
	}
	if _, err := Dividir(1, 0); err == nil {
		t.Errorf("Dividir(1, 0) tiene que devolver un error")
	}
}

func TestRetirarOk(t *testing.T) {
	stock := map[string]int{"yerba": 10}
	if got, err := Retirar(stock, "yerba", 3); err != nil || got != 7 {
		t.Errorf("Retirar(yerba, 3) = (%d, %v), quiero (7, nil)", got, err)
	}
	if stock["yerba"] != 7 {
		t.Errorf("el map tiene que quedar actualizado: yerba = %d, quiero 7", stock["yerba"])
	}
}

func TestRetirarErrores(t *testing.T) {
	if ErrStockInsuficiente == nil {
		t.Fatal("ErrStockInsuficiente no puede ser nil: crealo con errors.New")
	}
	stock := map[string]int{"yerba": 2}
	_, err := Retirar(stock, "yerba", 5)
	if !errors.Is(err, ErrStockInsuficiente) {
		t.Errorf("sin stock: el error %v tiene que envolver a ErrStockInsuficiente", err)
	}
	if err != nil && !strings.HasPrefix(err.Error(), "retirando 5 de yerba: ") {
		t.Errorf("mensaje = %q, tiene que empezar con %q", err.Error(), "retirando 5 de yerba: ")
	}
	if stock["yerba"] != 2 {
		t.Errorf("si falla, el stock no tiene que cambiar")
	}
	_, err = Retirar(stock, "café", 1)
	if err == nil || err.Error() != "producto café inexistente" {
		t.Errorf("producto inexistente: error = %v, quiero %q", err, "producto café inexistente")
	}
}

func TestParsearEdades(t *testing.T) {
	got, err := ParsearEdades([]string{"31", "7", "0"})
	if err != nil || !slices.Equal(got, []int{31, 7, 0}) {
		t.Errorf("ParsearEdades(ok) = (%v, %v), quiero ([31 7 0], nil)", got, err)
	}
	_, err = ParsearEdades([]string{"1", "x", "-3"})
	var numErr *strconv.NumError
	if err == nil || !strings.HasPrefix(err.Error(), "posición 1: ") || !errors.As(err, &numErr) {
		t.Errorf("con \"x\" en la posición 1: error = %v; quiero que empiece con "+
			"\"posición 1: \" y envuelva el error de strconv", err)
	}
	_, err = ParsearEdades([]string{"5", "-3"})
	if err == nil || err.Error() != "posición 1: edad negativa: -3" {
		t.Errorf("edad negativa: error = %v, quiero %q", err, "posición 1: edad negativa: -3")
	}
}
