package ejercicio

import (
	"maps"
	"reflect"
	"slices"
	"testing"
)

func TestContarPalabras(t *testing.T) {
	got := ContarPalabras("El perro y el gato  EL perro")
	want := map[string]int{"el": 3, "perro": 2, "y": 1, "gato": 1}
	if !maps.Equal(got, want) {
		t.Errorf("ContarPalabras = %v, quiero %v", got, want)
	}
}

func TestAgruparPorLargo(t *testing.T) {
	got := AgruparPorLargo([]string{"sol", "luna", "mar", "cielo", "rio"})
	want := map[int][]string{3: {"sol", "mar", "rio"}, 4: {"luna"}, 5: {"cielo"}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("AgruparPorLargo = %v, quiero %v", got, want)
	}
}

func TestInvertir(t *testing.T) {
	notas := map[string]int{"zoe": 9, "ana": 9, "beto": 7, "caro": 9}
	got := Invertir(notas)
	want := map[int][]string{9: {"ana", "caro", "zoe"}, 7: {"beto"}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Invertir = %v, quiero %v", got, want)
	}
}

func TestComunes(t *testing.T) {
	got := Comunes([]string{"go", "py", "rs", "go"}, []string{"js", "go", "rs", "rs"})
	if !slices.Equal(got, []string{"go", "rs"}) {
		t.Errorf("Comunes = %v, quiero [go rs]", got)
	}
	if got := Comunes([]string{"a"}, []string{"b"}); len(got) != 0 {
		t.Errorf("Comunes sin coincidencias = %v, quiero vacío", got)
	}
}
