// Formatear texto: fmt y strings.Builder.
//
// Agregá los imports que necesites (fmt, strings, ...).
package ejercicio

// Enumerar une los elementos al estilo español: "a", "a y b", "a, b y c".
// Sin elementos, "". Usá strings.Builder.
func Enumerar(items []string) string {
	// TODO
	return ""
}

// Item es un renglón de una factura.
type Item struct {
	Nombre string
	Precio float64
}

// TablaPrecios arma una tabla de ancho fijo, una línea por item, unidas con "\n":
//   - nombre alineado a la izquierda en 12 caracteres
//   - precio alineado a la derecha en 10, con 2 decimales
//   - al final una línea "TOTAL" con el mismo formato
//
// Ejemplo: "café           1500.50\nTOTAL          1500.50"
func TablaPrecios(items []Item) string {
	// TODO
	return ""
}

// Pesos representa un monto en centavos.
type Pesos int64

// String formatea con punto de miles y coma decimal: Pesos(123456789) → "$ 1.234.567,89".
// Los negativos llevan el signo después del "$ ": "$ -5,00".
func (p Pesos) String() string {
	// TODO
	return ""
}
