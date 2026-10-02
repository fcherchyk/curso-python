package ejercicio

import "testing"

func TestContarCaracteres(t *testing.T) {
	casos := map[string]int{"hola": 4, "año": 3, "ñandú": 5, "": 0, "日本": 2}
	for in, want := range casos {
		if got := ContarCaracteres(in); got != want {
			t.Errorf("ContarCaracteres(%q) = %d, quiero %d", in, got, want)
		}
	}
}

func TestInvertir(t *testing.T) {
	casos := map[string]string{"año": "oña", "hola": "aloh", "ñandú": "údnañ", "": ""}
	for in, want := range casos {
		if got := Invertir(in); got != want {
			t.Errorf("Invertir(%q) = %q, quiero %q", in, got, want)
		}
	}
}

func TestEsPalindromo(t *testing.T) {
	casos := map[string]bool{
		"Anita lava la tina":             true,
		"A man, a plan, a canal: Panama": true,
		"Ñu, ñu":                         false,
		"ñuñ":                            true,
		"python":                         false,
	}
	for in, want := range casos {
		if got := EsPalindromo(in); got != want {
			t.Errorf("EsPalindromo(%q) = %v, quiero %v", in, got, want)
		}
	}
}

func TestCapitalizar(t *testing.T) {
	casos := map[string]string{
		"  ÁRBOL de   navidad": "Árbol De Navidad",
		"go es lindo":          "Go Es Lindo",
		"ñandú":                "Ñandú",
	}
	for in, want := range casos {
		if got := Capitalizar(in); got != want {
			t.Errorf("Capitalizar(%q) = %q, quiero %q", in, got, want)
		}
	}
}
