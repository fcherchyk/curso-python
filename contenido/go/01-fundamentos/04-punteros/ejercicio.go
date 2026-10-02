// Punteros y paso por valor.
package ejercicio

// Intercambiar intercambia los valores apuntados por a y b.
func Intercambiar(a, b *int) {
	// TODO
}

// Cuenta es una cuenta bancaria simple.
type Cuenta struct {
	Titular string
	Saldo   int
}

// Depositar suma monto al saldo de la cuenta (tiene que verse afuera).
func Depositar(c *Cuenta, monto int) {
	// TODO
}

// NuevaCuenta crea una cuenta con saldo 0 y devuelve un puntero a ella.
func NuevaCuenta(titular string) *Cuenta {
	// TODO
	return nil
}

// Buscar devuelve un puntero a la PRIMERA cuenta del titular dado (para poder
// modificarla en el slice), o nil si no existe.
func Buscar(cuentas []Cuenta, titular string) *Cuenta {
	// TODO
	return nil
}

// DuplicarEnLugar multiplica por 2 cada elemento del slice, modificándolo.
func DuplicarEnLugar(xs []int) {
	// TODO
}
