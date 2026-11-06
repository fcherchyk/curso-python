# Agregaciones, estadística y aleatoriedad reproducible

Analizar datos es, en gran parte, **resumirlos**: promedios, desvíos, percentiles, máximos por
grupo. NumPy hace estas reducciones sobre cualquier eje de un array. Y para simular (Monte Carlo,
bootstrap, datos de prueba) necesitás números aleatorios **reproducibles**: que la misma
semilla produzca siempre los mismos resultados.

## Reducciones

```python
v = np.array([4, 8, 15, 16, 23, 42])
v.sum(), v.mean(), v.min(), v.max()
v.std()                 # desvío estándar poblacional (ddof=0)
v.std(ddof=1)           # muestral (divide por n-1): el que usan pandas y la estadística
np.median(v)
np.percentile(v, [25, 50, 75])     # cuartiles
np.cumsum(v)            # suma acumulada: [ 4 12 27 43 66 108]
np.cumprod(1 + rets)    # producto acumulado: crecimiento compuesto
```

> **`ddof`**: NumPy usa por defecto el desvío **poblacional** (`ddof=0`), y pandas, el
> **muestral** (`ddof=1`). Con pocos datos la diferencia se nota. Es una fuente clásica de
> discrepancias entre resultados.

## Reducir por eje

En una matriz, `axis` indica qué dimensión se **colapsa**:

```python
# 3 días (filas) x 4 productos (columnas)
ventas = np.array([[5, 2, 0, 7],
                   [3, 8, 1, 2],
                   [6, 1, 4, 9]])

ventas.sum(axis=0)       # [14 11  5 18]: total por PRODUCTO (colapsa los días)
ventas.sum(axis=1)       # [14 14 20]: total por DÍA (colapsa los productos)
ventas.argmax(axis=0)    # [2 1 2 2]: en qué día vendió más cada producto
ventas.max()             # 9: sobre todo el array
```

Pensalo así: `axis=0` recorre **hacia abajo** (un resultado por columna) y `axis=1`, **hacia la
derecha** (un resultado por fila).

### Valores faltantes: `nan`

```python
v = np.array([1.0, np.nan, 3.0])
v.mean()            # nan  ← un solo nan contamina todo
np.nanmean(v)       # 2.0  ← ignora los nan
np.isnan(v)         # [False  True False]
```

Existen versiones `nan*` de casi todas las reducciones (`nansum`, `nanstd`, `nanmax`…). pandas
las ignora por defecto.

## Números aleatorios: la API moderna

```python
rng = np.random.default_rng(42)        # un generador con semilla

rng.random(3)                          # 3 floats uniformes en [0, 1)
rng.integers(1, 7, size=10)            # 10 tiradas de dado (el 7 se excluye)
rng.normal(loc=0, scale=1, size=(2, 3))   # normal estándar en una matriz 2x3
rng.choice(["a", "b", "c"], size=5)    # elegir con reposición
rng.choice(v, size=len(v), replace=True)  # remuestreo (bootstrap)
rng.permutation(v), rng.shuffle(v)
```

- **Usá `default_rng`**. La API vieja (`np.random.seed(...)` + `np.random.rand`) usa un estado
  **global** compartido: cualquier librería que la use te cambia la secuencia.
- Pasá el generador (o la semilla) como **parámetro** a tus funciones. Así los tests son
  reproducibles y no hay estado global.
- La misma semilla con la misma secuencia de llamadas da siempre el mismo resultado.

```python
def simular(n: int, semilla: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(semilla)
    return rng.normal(size=n)

simular(3, semilla=1) == simular(3, semilla=1)   # todo True
```

## Monte Carlo y bootstrap en dos líneas

```python
# Probabilidad de sacar más de 10 sumando dos dados
rng = np.random.default_rng(0)
tiradas = rng.integers(1, 7, size=(100_000, 2)).sum(axis=1)
(tiradas > 10).mean()            # ≈ 0.0833 (3/36)

# Bootstrap: incertidumbre de la media de una muestra
medias = rng.choice(muestra, size=(10_000, len(muestra))).mean(axis=1)
np.percentile(medias, [2.5, 97.5])      # intervalo de confianza del 95 %
```

Generar **todas** las simulaciones en una matriz y reducir por eje es mucho más rápido que un
bucle con una simulación por vuelta. Es la misma vectorización de antes, aplicada a la
estadística. En el módulo de finanzas la usamos para la frontera eficiente.

## Resumen

- `sum`, `mean`, `std` (¡`ddof`!), `median`, `percentile`, `cumsum` y `cumprod`.
- `axis=0` da un resultado por columna y `axis=1`, uno por fila; `argmax(axis=...)` para
  "dónde".
- `nan` contamina: usá `nanmean` y compañía.
- `rng = np.random.default_rng(semilla)` y pasalo como parámetro; nada de `np.random.seed`.
- Monte Carlo y bootstrap vectorizados: generar todo en una matriz y reducir.

## Ejercicio

Resúmenes por eje, el mejor día por producto, una simulación de dados y un bootstrap, ambos
reproducibles con semilla.

**Para profundizar:** [Statistics](https://numpy.org/doc/stable/reference/routines.statistics.html),
[Random Generator](https://numpy.org/doc/stable/reference/random/generator.html).
