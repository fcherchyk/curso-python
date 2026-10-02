package ejercicio

import (
	"slices"
	"testing"
)

func TestRango(t *testing.T) {
	if got := slices.Collect(Rango(0, 10, 3)); !slices.Equal(got, []int{0, 3, 6, 9}) {
		t.Errorf("Rango(0, 10, 3) = %v, quiero [0 3 6 9]", got)
	}
	if got := slices.Collect(Rango(5, 5, 1)); len(got) != 0 {
		t.Errorf("Rango(5, 5, 1) = %v, quiero vacío", got)
	}
	if got := slices.Collect(Rango(0, 3, 0)); len(got) != 0 {
		t.Errorf("Rango con paso 0 = %v, quiero vacío", got)
	}
}

func TestRangoRespetaBreak(t *testing.T) {
	var vistos []int
	for n := range Rango(0, 100, 1) {
		if n == 3 {
			break // si el iterador ignora el false de yield, esto hace panic
		}
		vistos = append(vistos, n)
	}
	if !slices.Equal(vistos, []int{0, 1, 2}) {
		t.Errorf("con break en 3 = %v, quiero [0 1 2]", vistos)
	}
}

func TestFibonacciInfinito(t *testing.T) {
	var got []int
	for n := range Fibonacci() {
		if len(got) == 10 {
			break
		}
		got = append(got, n)
	}
	if !slices.Equal(got, []int{0, 1, 1, 2, 3, 5, 8, 13, 21, 34}) {
		t.Errorf("primeros 10 de Fibonacci = %v", got)
	}
}

func TestTomar(t *testing.T) {
	if got := slices.Collect(Tomar(Fibonacci(), 6)); !slices.Equal(got, []int{0, 1, 1, 2, 3, 5}) {
		t.Errorf("Tomar(Fibonacci(), 6) = %v, quiero [0 1 1 2 3 5]", got)
	}
	if got := slices.Collect(Tomar(Rango(0, 2, 1), 5)); !slices.Equal(got, []int{0, 1}) {
		t.Errorf("Tomar con menos elementos = %v, quiero [0 1]", got)
	}
}

func TestEnumerar(t *testing.T) {
	var got []string
	for i, s := range Enumerar([]string{"a", "b", "c"}, 1) {
		got = append(got, string(rune('0'+i))+s)
	}
	if !slices.Equal(got, []string{"1a", "2b", "3c"}) {
		t.Errorf("Enumerar = %v, quiero [1a 2b 3c]", got)
	}
}
