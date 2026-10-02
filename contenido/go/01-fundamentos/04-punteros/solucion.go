package ejercicio

func Intercambiar(a, b *int) {
	*a, *b = *b, *a
}

type Cuenta struct {
	Titular string
	Saldo   int
}

func Depositar(c *Cuenta, monto int) {
	c.Saldo += monto
}

func NuevaCuenta(titular string) *Cuenta {
	return &Cuenta{Titular: titular}
}

func Buscar(cuentas []Cuenta, titular string) *Cuenta {
	for i := range cuentas {
		// &cuentas[i] apunta al elemento; con `for _, c := range` sería una copia.
		if cuentas[i].Titular == titular {
			return &cuentas[i]
		}
	}
	return nil
}

func DuplicarEnLugar(xs []int) {
	for i := range xs {
		xs[i] *= 2
	}
}
