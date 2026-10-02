package ejercicio

import (
	"reflect"
	"slices"
	"testing"
)

func TestFiltrar(t *testing.T) {
	xs := []int{1, 2, 3, 4, 5, 6}
	got := Filtrar(xs, func(n int) bool { return n%2 == 0 })
	if !slices.Equal(got, []int{2, 4, 6}) {
		t.Errorf("Filtrar(pares) = %v, quiero [2 4 6]", got)
	}
	if !slices.Equal(xs, []int{1, 2, 3, 4, 5, 6}) {
		t.Errorf("Filtrar modificó el original: %v", xs)
	}
}

func TestInvertir(t *testing.T) {
	casos := [][2][]int{
		{{1, 2, 3}, {3, 2, 1}},
		{{1, 2, 3, 4}, {4, 3, 2, 1}},
		{{7}, {7}},
	}
	for _, c := range casos {
		xs := slices.Clone(c[0])
		Invertir(xs)
		if !slices.Equal(xs, c[1]) {
			t.Errorf("Invertir(%v) → %v, quiero %v", c[0], xs, c[1])
		}
	}
}

func TestEnLotes(t *testing.T) {
	got := EnLotes([]int{1, 2, 3, 4, 5, 6, 7}, 3)
	want := [][]int{{1, 2, 3}, {4, 5, 6}, {7}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("EnLotes(1..7, 3) = %v, quiero %v", got, want)
	}
	if got := EnLotes([]int{1, 2}, 0); got != nil {
		t.Errorf("EnLotes(xs, 0) = %v, quiero nil", got)
	}
}

func TestAgregarCopiaSinAliasing(t *testing.T) {
	base := make([]int, 2, 10) // capacidad libre: el append ingenuo compartiría memoria
	base[0], base[1] = 1, 2
	x := AgregarCopia(base, 9)
	y := AgregarCopia(base, 7)
	if !slices.Equal(x, []int{1, 2, 9}) || !slices.Equal(y, []int{1, 2, 7}) {
		t.Fatalf("x = %v, y = %v; quiero [1 2 9] y [1 2 7] (¿compartieron memoria?)", x, y)
	}
	x[0] = 100
	if base[0] != 1 {
		t.Errorf("modificar el resultado cambió la base: %v", base)
	}
}
