package ejercicio

import (
	"slices"
	"testing"
)

func TestFizzBuzz(t *testing.T) {
	got := FizzBuzz(15)
	want := []string{"1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
		"11", "Fizz", "13", "14", "FizzBuzz"}
	if !slices.Equal(got, want) {
		t.Errorf("FizzBuzz(15) = %q\nquiero %q", got, want)
	}
	if got := FizzBuzz(0); len(got) != 0 {
		t.Errorf("FizzBuzz(0) = %q, quiero vacío", got)
	}
}

func TestClasificar(t *testing.T) {
	casos := []struct {
		t    float64
		want string
	}{{-5, "frío"}, {9.9, "frío"}, {10, "templado"}, {24.9, "templado"}, {25, "calor"}}
	for _, c := range casos {
		if got := Clasificar(c.t); got != c.want {
			t.Errorf("Clasificar(%v) = %q, quiero %q", c.t, got, c.want)
		}
	}
}

func TestEsPrimo(t *testing.T) {
	var primos []int
	for n := range 30 {
		if EsPrimo(n) {
			primos = append(primos, n)
		}
	}
	want := []int{2, 3, 5, 7, 11, 13, 17, 19, 23, 29}
	if !slices.Equal(primos, want) {
		t.Errorf("primos menores que 30 = %v, quiero %v", primos, want)
	}
	if !EsPrimo(7919) || EsPrimo(7917) || EsPrimo(-7) {
		t.Errorf("falla con 7919 (primo), 7917 (no primo) o -7 (no primo)")
	}
}

func TestBuscar(t *testing.T) {
	m := [][]int{{1, 2, 3}, {4, 5, 6}, {7, 5, 9}}
	if f, c, ok := Buscar(m, 5); !ok || f != 1 || c != 1 {
		t.Errorf("Buscar(m, 5) = (%d, %d, %v), quiero (1, 1, true)", f, c, ok)
	}
	if f, c, ok := Buscar(m, 9); !ok || f != 2 || c != 2 {
		t.Errorf("Buscar(m, 9) = (%d, %d, %v), quiero (2, 2, true)", f, c, ok)
	}
	if _, _, ok := Buscar(m, 42); ok {
		t.Errorf("Buscar(m, 42) encontró algo que no está")
	}
}
