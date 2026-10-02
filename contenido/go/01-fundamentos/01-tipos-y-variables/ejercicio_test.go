package ejercicio

import (
	"math"
	"testing"
)

func casi(a, b float64) bool { return math.Abs(a-b) < 1e-9 }

func TestCelsiusAFahrenheit(t *testing.T) {
	casos := []struct{ c, f float64 }{{0, 32}, {100, 212}, {-40, -40}, {36.6, 97.88}}
	for _, caso := range casos {
		if got := CelsiusAFahrenheit(caso.c); !casi(got, caso.f) {
			t.Errorf("CelsiusAFahrenheit(%v) = %v, quiero %v", caso.c, got, caso.f)
		}
	}
}

func TestPromedio(t *testing.T) {
	casos := []struct {
		nums []int
		want float64
	}{
		{[]int{1, 2}, 1.5},
		{[]int{10, 20, 30}, 20},
		{[]int{7}, 7},
		{nil, 0},
	}
	for _, caso := range casos {
		if got := Promedio(caso.nums); !casi(got, caso.want) {
			t.Errorf("Promedio(%v) = %v, quiero %v", caso.nums, got, caso.want)
		}
	}
}

func TestNombreDia(t *testing.T) {
	casos := map[Dia]string{
		Lunes: "lunes", Miercoles: "miércoles", Sabado: "sábado", Domingo: "domingo",
		Dia(7): "desconocido", Dia(-1): "desconocido",
	}
	for d, want := range casos {
		if got := NombreDia(d); got != want {
			t.Errorf("NombreDia(%d) = %q, quiero %q", d, got, want)
		}
	}
}

func TestEsFinDeSemana(t *testing.T) {
	for d := Lunes; d <= Domingo; d++ {
		want := d == Sabado || d == Domingo
		if got := EsFinDeSemana(d); got != want {
			t.Errorf("EsFinDeSemana(%d) = %v, quiero %v", d, got, want)
		}
	}
}
