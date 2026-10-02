package ejercicio

import (
	"fmt"
	"testing"
)

func TestEnumerar(t *testing.T) {
	casos := []struct {
		in   []string
		want string
	}{
		{[]string{"pan"}, "pan"},
		{[]string{"pan", "leche"}, "pan y leche"},
		{[]string{"pan", "leche", "yerba", "café"}, "pan, leche, yerba y café"},
		{nil, ""},
	}
	for _, c := range casos {
		if got := Enumerar(c.in); got != c.want {
			t.Errorf("Enumerar(%q) = %q, quiero %q", c.in, got, c.want)
		}
	}
}

func TestTablaPrecios(t *testing.T) {
	got := TablaPrecios([]Item{{"café", 1500.5}, {"medialunas", 12}})
	want := "café           1500.50\nmedialunas       12.00\nTOTAL          1512.50"
	if got != want {
		t.Errorf("TablaPrecios =\n%s\nquiero\n%s", got, want)
	}
}

func TestPesosString(t *testing.T) {
	casos := map[Pesos]string{
		123456789: "$ 1.234.567,89",
		150:       "$ 1,50",
		5:         "$ 0,05",
		100000:    "$ 1.000,00",
		-500:      "$ -5,00",
	}
	for p, want := range casos {
		if got := p.String(); got != want {
			t.Errorf("Pesos(%d).String() = %q, quiero %q", int64(p), got, want)
		}
	}
	if got := fmt.Sprintf("total: %v", Pesos(1999)); got != "total: $ 19,99" {
		t.Errorf("fmt tiene que usar String(): %q", got)
	}
}
