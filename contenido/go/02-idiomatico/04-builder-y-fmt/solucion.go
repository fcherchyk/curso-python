package ejercicio

import (
	"fmt"
	"strconv"
	"strings"
)

func Enumerar(items []string) string {
	var b strings.Builder
	for i, item := range items {
		switch {
		case i == 0:
		case i == len(items)-1:
			b.WriteString(" y ")
		default:
			b.WriteString(", ")
		}
		b.WriteString(item)
	}
	return b.String()
}

type Item struct {
	Nombre string
	Precio float64
}

func TablaPrecios(items []Item) string {
	var b strings.Builder
	total := 0.0
	for _, it := range items {
		fmt.Fprintf(&b, "%-12s%10.2f\n", it.Nombre, it.Precio)
		total += it.Precio
	}
	fmt.Fprintf(&b, "%-12s%10.2f", "TOTAL", total)
	return b.String()
}

type Pesos int64

func (p Pesos) String() string {
	signo := ""
	if p < 0 {
		signo, p = "-", -p
	}
	enteros := strconv.FormatInt(int64(p/100), 10)
	// Insertamos un punto cada tres dígitos, de derecha a izquierda.
	var conPuntos strings.Builder
	for i, d := range enteros {
		if i > 0 && (len(enteros)-i)%3 == 0 {
			conPuntos.WriteByte('.')
		}
		conPuntos.WriteRune(d)
	}
	return fmt.Sprintf("$ %s%s,%02d", signo, conPuntos.String(), p%100)
}
