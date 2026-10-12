# Precios y retornos

En finanzas casi nunca se trabaja con precios directamente, sino con **retornos**: cuánto
cambió el precio en proporción. Un precio de 100 contra uno de 50 no dice nada. Que ambos
subieron un 2 % ayer sí permite compararlos. Este capítulo arma la base de todo el módulo.

## Los datos

Cada capítulo trae `precios.csv`: precios de cierre diarios **sintéticos** de cuatro acciones
inventadas (`ACME`, `BETA`, `CIRC`, `DELTA`) y un índice de mercado (`INDICE`), entre 2023 y
2025. Son sintéticos para que los tests sean reproducibles y no dependan de internet. Con datos
reales el código es idéntico:

```python
import yfinance as yf                                        # pip install yfinance
precios = yf.download(["AAPL", "MSFT", "SPY"], start="2023-01-01")["Close"]
```

```python
precios = pd.read_csv("precios.csv", parse_dates=["fecha"], index_col="fecha")
precios.shape          # (783, 5): ~252 días hábiles por año
```

Solo hay **días hábiles**: un año bursátil tiene unas **252** ruedas. Ese número aparece cada
vez que se anualiza algo.

## Retorno simple

```text
r_t = P_t / P_{t-1} - 1
```

```python
retornos = precios.pct_change().dropna()   # el primer día no tiene anterior: NaN
```

```
              ACME    BETA    CIRC   DELTA  INDICE
fecha
2023-01-03  0.0225  0.0248  0.0263  0.0078  0.0170
2023-01-04  0.0179  0.0145  0.0052  0.0037  0.0119
```

Propiedades:

- **Se agregan entre activos**: el retorno de un portafolio es el promedio ponderado de los
  retornos simples de sus activos (lo vamos a usar en el capítulo de portafolios).
- **No se suman en el tiempo**: +10 % y luego −10 % no da 0 sino 1.1 × 0.9 − 1 = −1 %.
  Se **componen**: el acumulado es el producto.

```python
acumulado = (1 + retornos).prod() - 1      # ACME: 0.4118 → +41.18 % en todo el período
curva = (1 + retornos).cumprod()           # evolución de $1 invertido
```

## Retorno logarítmico

```text
l_t = ln(P_t / P_{t-1}) = ln(1 + r_t)
```

```python
log_ret = np.log(precios / precios.shift(1)).dropna()
```

- **Se suman en el tiempo**: el log-retorno de todo el período es la suma de los diarios.
  `log_ret.sum()` en ACME da 0.3449, y `np.exp(0.3449) - 1` da 0.4118, el mismo acumulado.
- Para cambios chicos, `l ≈ r`. Con cambios grandes divergen.
- **No se agregan entre activos**: el log-retorno de un portafolio no es el promedio de los
  log-retornos.

Regla práctica: **simples para portafolios** y **log para sumar en el tiempo o para modelos
estadísticos**.

## Anualizar

Un retorno total del 41 % en tres años no se compara directamente con uno del 15 % en uno.
Hay que llevarlos a una base común, el **año**:

```text
R_anual = (1 + R_total) ^ (252 / n) - 1
```

con `n` la cantidad de retornos diarios. Es interés compuesto al revés.

```python
anual = (1 + retornos).prod() ** (252 / len(retornos)) - 1    # ACME: 0.1175
```

**No** multipliques el retorno diario promedio por 252: ignora la composición y sobreestima
cuando hay volatilidad.

## CAGR

La **tasa de crecimiento anual compuesta** es la misma idea, pero medida con fechas de calendario
en lugar de contar ruedas:

```text
CAGR = (P_final / P_inicial) ^ (1 / años) - 1
```

```python
anios = (precios.index[-1] - precios.index[0]).days / 365.25
cagr = (precios.iloc[-1] / precios.iloc[0]) ** (1 / anios) - 1   # ACME: 0.122
```

La diferencia con el anterior (0.1175 contra 0.122) viene de que el CSV empieza con el precio
del 2 de enero, sin el retorno de ese día, y de la convención de días. En la práctica, elegí una
convención y usala de forma consistente.

## Resumen

- `pct_change()` para retornos simples y `np.log(p / p.shift())` para logarítmicos; `dropna()`.
- Simples: se ponderan entre activos y se componen en el tiempo (`(1 + r).prod() - 1`).
- Log: se suman en el tiempo; `exp(suma) - 1` vuelve al simple.
- Anualizá componiendo: `(1 + R)^(252/n) - 1`; CAGR con fechas de calendario.

## Ejercicio

Calculá retornos simples y logarítmicos, el acumulado, el retorno anualizado y el CAGR.

**Para profundizar:** *Python for Finance* (Yves Hilpisch), cap. "Financial Time Series";
[pandas: pct_change](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html).
