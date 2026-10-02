package ejercicio

import (
	"slices"
	"testing"
)

func TestMinMax(t *testing.T) {
	if min, max, ok := MinMax(3, -1, 7, 2); min != -1 || max != 7 || !ok {
		t.Errorf("MinMax(3, -1, 7, 2) = (%d, %d, %v), quiero (-1, 7, true)", min, max, ok)
	}
	if min, max, ok := MinMax(5); min != 5 || max != 5 || !ok {
		t.Errorf("MinMax(5) = (%d, %d, %v), quiero (5, 5, true)", min, max, ok)
	}
	xs := []int{4, 9}
	if min, max, _ := MinMax(xs...); min != 4 || max != 9 {
		t.Errorf("MinMax(xs...) = (%d, %d), quiero (4, 9)", min, max)
	}
	if _, _, ok := MinMax(); ok {
		t.Errorf("MinMax() sin argumentos tiene que devolver ok = false")
	}
}

func TestMap(t *testing.T) {
	xs := []int{1, 2, 3}
	got := Map(xs, func(x int) int { return x * x })
	if !slices.Equal(got, []int{1, 4, 9}) {
		t.Errorf("Map(cuadrado) = %v, quiero [1 4 9]", got)
	}
	if !slices.Equal(xs, []int{1, 2, 3}) {
		t.Errorf("Map modificó el slice original: %v", xs)
	}
	if got := Map(nil, func(x int) int { return x }); len(got) != 0 {
		t.Errorf("Map(nil) = %v, quiero vacío", got)
	}
}

func TestNuevoContador(t *testing.T) {
	a, b := NuevoContador(0), NuevoContador(10)
	got := []int{a(), a(), a(), b(), b(), a()}
	want := []int{0, 1, 2, 10, 11, 3}
	if !slices.Equal(got, want) {
		t.Errorf("secuencia de contadores = %v, quiero %v", got, want)
	}
}

func TestComponer(t *testing.T) {
	doble := func(x int) int { return x * 2 }
	masUno := func(x int) int { return x + 1 }
	if got := Componer(doble, masUno)(3); got != 8 {
		t.Errorf("Componer(doble, masUno)(3) = %d, quiero 8", got)
	}
	if got := Componer(masUno, doble)(3); got != 7 {
		t.Errorf("Componer(masUno, doble)(3) = %d, quiero 7", got)
	}
}
