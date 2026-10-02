package ejercicio

import (
	"slices"
	"testing"
)

func TestOrdenarPersonas(t *testing.T) {
	ps := []Persona{{"Zoe", 30}, {"Ana", 25}, {"Beto", 30}, {"Caro", 40}}
	OrdenarPersonas(ps)
	want := []Persona{{"Caro", 40}, {"Beto", 30}, {"Zoe", 30}, {"Ana", 25}}
	if !slices.Equal(ps, want) {
		t.Errorf("OrdenarPersonas = %v, quiero %v", ps, want)
	}
}

func TestMasCaro(t *testing.T) {
	ps := []Producto{{"pan", 1.2}, {"café", 9.8}, {"té", 9.8}}
	if got, ok := MasCaro(ps); !ok || got.Nombre != "café" {
		t.Errorf("MasCaro = (%v, %v), quiero ({café 9.8}, true)", got, ok)
	}
	if _, ok := MasCaro(nil); ok {
		t.Errorf("MasCaro(nil) tiene que devolver ok = false")
	}
}

func TestClavesOrdenadas(t *testing.T) {
	got := ClavesOrdenadas(map[string]int{"pera": 1, "banana": 2, "uva": 3})
	if !slices.Equal(got, []string{"banana", "pera", "uva"}) {
		t.Errorf("ClavesOrdenadas = %v, quiero [banana pera uva]", got)
	}
}

func TestTopN(t *testing.T) {
	xs := []int{5, 1, 9, 3, 7}
	if got := TopN(xs, 3); !slices.Equal(got, []int{9, 7, 5}) {
		t.Errorf("TopN(xs, 3) = %v, quiero [9 7 5]", got)
	}
	if !slices.Equal(xs, []int{5, 1, 9, 3, 7}) {
		t.Errorf("TopN modificó el original: %v", xs)
	}
	if got := TopN([]int{2, 1}, 5); !slices.Equal(got, []int{2, 1}) {
		t.Errorf("TopN con menos de n = %v, quiero [2 1]", got)
	}
}
