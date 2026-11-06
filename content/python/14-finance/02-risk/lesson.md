# Riesgo: volatilidad, drawdown y VaR

Un retorno alto no dice nada sin el riesgo que hubo que correr para obtenerlo. "Riesgo" no es
una sola cosa, y cada medida responde a una pregunta distinta:

| Pregunta                                            | Medida                 |
|-----------------------------------------------------|------------------------|
| ¿Cuánto oscila en un año típico?                     | volatilidad anualizada |
| ¿Cuál fue la peor caída desde un máximo?              | drawdown máximo        |
| ¿Cuánto puedo perder en un mal día (con 95 % de confianza)? | VaR             |
| Y en los días que superan el VaR, ¿cuánto pierdo en promedio? | CVaR / Expected Shortfall |

Usamos los retornos simples diarios del capítulo anterior: `r = precios.pct_change().dropna()`.

## Volatilidad

Es el **desvío estándar de los retornos**. Mide cuánto se alejan del promedio, para arriba y
para abajo.

```python
vol_diaria = r.std()
vol_anual = r.std() * np.sqrt(252)
```

```
ACME 0.269   BETA 0.176   CIRC 0.382   DELTA 0.107   INDICE 0.160
```

¿Por qué `√252` y no `252`? Si los retornos diarios son independientes, las **varianzas** se
suman: la varianza anual es 252 veces la diaria, y el desvío es la raíz. Esta es la "regla de la
raíz del tiempo". Con 16 % de volatilidad anual, el INDICE se mueve típicamente ±1 % por día
(0.16 / √252 ≈ 0.010).

Limitaciones: castiga igual las subas y las bajas, y supone algo parecido a una distribución
normal. Los mercados reales tienen **colas gordas**: los días extremos son mucho más frecuentes
de lo que la normal predice.

## Drawdown

El **drawdown** es cuánto estás por debajo del **máximo anterior**. Es la medida que más se
parece a lo que siente un inversor ("¿cuánto perdí desde el pico?").

```python
pico = precios.cummax()                  # máximo acumulado hasta cada fecha
drawdown = precios / pico - 1            # 0 en máximos, negativo en las caídas
max_dd = drawdown.min()                  # CIRC: −0.51
```

CIRC llegó a estar **51 % abajo** de su máximo (del 6/9/2023 al 17/6/2024). Para recuperar una
caída del 51 % hay que **subir 104 %**: 1 / (1 − 0.51) − 1. Por eso las caídas grandes son tan
dañinas, y por eso el drawdown importa más que la volatilidad para muchos inversores.

## VaR histórico

El **Value at Risk** al 95 % responde: *"en 95 de cada 100 días, la pérdida no supera X"*. La
versión **histórica** no supone ninguna distribución: toma el percentil 5 de los retornos
observados.

```python
var_95 = -r.quantile(0.05)       # ACME: 0.0284 → en el 5 % de los peores días pierde ≥ 2.84 %
```

Se suele expresar como pérdida **positiva**, de ahí el signo menos. Con una posición de
$100 000 en ACME, el VaR diario al 95 % es de unos $2 840.

El VaR **no dice cuánto se pierde en ese 5 %**: podría ser 3 % o 30 %. Para eso está el CVaR.

## CVaR (Expected Shortfall)

El promedio de los retornos **en los días que superan el VaR**:

```python
q = r.quantile(0.05)
cvar_95 = -r[r <= q].mean()      # ACME: 0.0345
```

Es siempre mayor o igual al VaR y describe mejor la cola. Los reguladores bancarios (Basilea)
pasaron del VaR al Expected Shortfall justamente por eso.

## Resumen

- Volatilidad: `r.std() * √252`. Mide oscilación simétrica y supone colas normales.
- Drawdown: `p / p.cummax() - 1`; el máximo drawdown es su mínimo. Una caída del 50 % exige
  un +100 % para recuperarse.
- VaR histórico: `-r.quantile(1 - nivel)`, la pérdida que no se supera en el `nivel` % de los días.
- CVaR: el promedio de las pérdidas en los días que superan el VaR.
- **Todo es histórico**: el riesgo pasado no garantiza el futuro.

## Ejercicio

Implementá la volatilidad anualizada, la serie de drawdown, el drawdown máximo, el VaR y el CVaR
históricos.

**Para profundizar:** [Investopedia: Value at Risk](https://www.investopedia.com/terms/v/var.asp),
*Fooled by Randomness* (N. N. Taleb) sobre las colas gordas.
