# Frontera eficiente por Monte Carlo

El capítulo anterior calculaba el riesgo y el retorno de **un** portafolio. La pregunta natural
es: **¿cuáles son los mejores pesos?** Harry Markowitz respondió en 1952 (y ganó el Nobel): no
hay un único "mejor", sino una **frontera eficiente**, el conjunto de portafolios que dan el
máximo retorno posible para cada nivel de riesgo.

## La idea con Monte Carlo

La forma rigurosa es un problema de optimización (`scipy.optimize.minimize` o `cvxpy`). La forma
intuitiva, y la que usamos acá, es **probar muchos portafolios al azar** y mirar la nube:

```python
rng = np.random.default_rng(42)            # semilla: resultados reproducibles
W = rng.random((5000, 4))                  # 5000 portafolios × 4 activos, en [0, 1)
W /= W.sum(axis=1, keepdims=True)          # normalizar: cada fila suma 1 (sin ventas en corto)
```

`keepdims=True` deja la suma con forma `(5000, 1)`, así el **broadcasting** del módulo 11 divide
cada fila por su propia suma.

## Retorno y volatilidad de 5000 portafolios a la vez

Nada de `for`: la vectorización de NumPy calcula todos juntos.

```python
mu = r.mean().to_numpy() * 252            # retornos esperados anuales (4,)
cov = r.cov().to_numpy() * 252            # covarianza anual (4, 4)

retornos = W @ mu                                          # (5000,)
vols = np.sqrt(np.einsum("ij,jk,ik->i", W, cov, W))       # wᵢᵀ Σ wᵢ para cada fila
sharpes = (retornos - 0.04) / vols
```

`einsum` describe la operación con índices: para cada portafolio `i`, suma `W[i,j]·cov[j,k]·W[i,k]`
sobre `j` y `k`. Es `wᵀΣw` aplicado fila por fila. Una alternativa equivalente es
`((W @ cov) * W).sum(axis=1)`.

## Los dos portafolios notables

```python
i = sharpes.argmax()      # máximo Sharpe: el mejor retorno por unidad de riesgo
j = vols.argmin()         # mínima varianza: el menos riesgoso
```

| | ACME | BETA | CIRC | DELTA | retorno | vol | Sharpe |
|---|---|---|---|---|---|---|---|
| máximo Sharpe   | 0.087 | 0.023 | 0.055 | 0.835 | 0.146 | 0.112 | 0.95 |
| mínima varianza | 0.053 | 0.252 | 0.006 | 0.689 | 0.104 | 0.107 | 0.59 |

Ambos cargan mucho DELTA: baja volatilidad, buen retorno y poca correlación con el resto.

## La nube y su borde


Al graficar volatilidad (X) contra retorno (Y), la nube tiene un **borde superior izquierdo**:
esa es la frontera eficiente. Cualquier portafolio que esté por debajo es **ineficiente**,
porque hay otro con el mismo riesgo y más retorno. El de máximo Sharpe es el punto de la
frontera donde toca la recta que sale de la tasa libre de riesgo (la *capital market line*).

## Advertencias importantes

- **Las entradas son estimaciones históricas**, y los retornos esperados son ruidosísimos. Con
  otro período, los pesos "óptimos" cambian por completo. La optimización de Markowitz es
  famosa por **amplificar los errores de estimación** ("error maximization").
- Por eso, en la práctica se usan restricciones (pesos máximos), estimadores más robustos o
  enfoques que no dependen de los retornos esperados (mínima varianza, *risk parity*).
- Monte Carlo es aproximado: con muchos activos, los portafolios aleatorios casi nunca llegan
  al borde. Ahí hace falta un optimizador.

## Resumen

- Generá pesos aleatorios con `default_rng(semilla)` y normalizá las filas con `keepdims=True`.
- Retornos: `W @ mu`. Varianzas: `einsum("ij,jk,ik->i", W, cov, W)`.
- Máximo Sharpe con `argmax` y mínima varianza con `argmin` sobre la volatilidad.
- La frontera es el borde superior de la nube riesgo-retorno.
- Los pesos óptimos son muy sensibles a las estimaciones: desconfiá de ellos.

## Ejercicio

Generá pesos aleatorios reproducibles, simulá portafolios, encontrá los de máximo Sharpe y
mínima varianza y graficá la nube marcando ambos.

**Para profundizar:** [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/) (optimización
real); [numpy.einsum](https://numpy.org/doc/stable/reference/generated/numpy.einsum.html).
