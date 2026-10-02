package ejercicio

import "testing"

func TestSumarNumeros(t *testing.T) {
	if got, err := SumarNumeros("1, 2,3 ,  4"); err != nil || got != 10 {
		t.Errorf(`SumarNumeros("1, 2,3 ,  4") = (%d, %v), quiero (10, nil)`, got, err)
	}
	if got, err := SumarNumeros("-5,5"); err != nil || got != 0 {
		t.Errorf(`SumarNumeros("-5,5") = (%d, %v), quiero (0, nil)`, got, err)
	}
	if _, err := SumarNumeros("1,dos,3"); err == nil {
		t.Errorf(`SumarNumeros("1,dos,3") tiene que devolver un error`)
	}
}

func TestIniciales(t *testing.T) {
	casos := map[string]string{
		"ana maría pérez": "AMP",
		"  beto   ":       "B",
		"élida óvalo":     "ÉÓ",
		"":                "",
	}
	for in, want := range casos {
		if got := Iniciales(in); got != want {
			t.Errorf("Iniciales(%q) = %q, quiero %q", in, got, want)
		}
	}
}

func TestHipotenusa(t *testing.T) {
	casos := []struct{ a, b, want float64 }{{3, 4, 5}, {1, 1, 1.41}, {5, 12, 13}}
	for _, c := range casos {
		if got := Hipotenusa(c.a, c.b); got != c.want {
			t.Errorf("Hipotenusa(%v, %v) = %v, quiero %v", c.a, c.b, got, c.want)
		}
	}
}

func TestEsIdentificadorExportado(t *testing.T) {
	casos := map[string]bool{"Sumar": true, "sumar": false, "Ñandú": true, "_x": false, "": false}
	for in, want := range casos {
		if got := EsIdentificadorExportado(in); got != want {
			t.Errorf("EsIdentificadorExportado(%q) = %v, quiero %v", in, got, want)
		}
	}
}
