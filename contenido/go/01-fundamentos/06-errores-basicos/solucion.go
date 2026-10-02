package ejercicio

import (
	"errors"
	"fmt"
	"strconv"
)

func Dividir(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("división por cero")
	}
	return a / b, nil
}

var ErrStockInsuficiente = errors.New("stock insuficiente")

func Retirar(stock map[string]int, nombre string, cantidad int) (int, error) {
	disponible, ok := stock[nombre]
	if !ok {
		return 0, fmt.Errorf("producto %s inexistente", nombre)
	}
	if cantidad > disponible {
		return disponible, fmt.Errorf("retirando %d de %s: %w", cantidad, nombre, ErrStockInsuficiente)
	}
	stock[nombre] = disponible - cantidad
	return stock[nombre], nil
}

func ParsearEdades(textos []string) ([]int, error) {
	edades := make([]int, 0, len(textos))
	for i, texto := range textos {
		n, err := strconv.Atoi(texto)
		if err != nil {
			return nil, fmt.Errorf("posición %d: %w", i, err)
		}
		if n < 0 {
			return nil, fmt.Errorf("posición %d: edad negativa: %d", i, n)
		}
		edades = append(edades, n)
	}
	return edades, nil
}
