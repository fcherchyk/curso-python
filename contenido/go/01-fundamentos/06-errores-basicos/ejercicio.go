// Errores: valores, no excepciones.
//
// Agregá los imports que necesites (errors, fmt, strconv, ...).
package ejercicio

// Dividir devuelve a / b, o un error si b es 0.
func Dividir(a, b float64) (float64, error) {
	// TODO
	return 0, nil
}

// ErrStockInsuficiente se devuelve cuando no alcanza el stock.
// Completá: tiene que ser un error creado con errors.New (hoy es nil).
var ErrStockInsuficiente error

// Retirar descuenta cantidad del stock del producto y devuelve el stock restante.
//   - Si el producto no existe en el map: error con el mensaje "producto <nombre> inexistente".
//   - Si no alcanza: un error que ENVUELVA a ErrStockInsuficiente, con el mensaje
//     "retirando <cantidad> de <nombre>: " + el mensaje del centinela.
func Retirar(stock map[string]int, nombre string, cantidad int) (int, error) {
	// TODO
	return 0, nil
}

// ParsearEdades convierte textos a edades. Corta en el PRIMER error y lo devuelve
// envuelto con la posición: "posición <i>: <error original>".
// Una edad negativa también es un error ("edad negativa: <n>").
func ParsearEdades(textos []string) ([]int, error) {
	// TODO
	return nil, nil
}
