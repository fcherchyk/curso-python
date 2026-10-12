# Portafolios: pesos, covarianza y diversificación

Casi nadie invierte en un solo activo. Un **portafolio** es una combinación con **pesos** (qué
fracción del capital va a cada activo), y tiene una propiedad casi mágica: su riesgo es **menor
que el promedio** de los riesgos de sus partes. En este capítulo usamos solo las cuatro acciones
(sin el INDICE).

## Pesos y retorno

```python
activos = ["ACME", "BETA", "CIRC", "DELTA"]
pesos = pd.Series(0.25, index=activos)      # partes iguales; deben sumar 1
r = precios[activos].pct_change().dropna()

r_port = r @ pesos                          # retorno diario del portafolio: Σ wᵢ·rᵢ
```

Como el retorno simple se **agrega entre activos** (capítulo 1), el retorno del portafolio es
el promedio ponderado. El retorno esperado anual es `pesos @ r.mean() * 252` (0.1216 con pesos
iguales).

## Riesgo: la matriz de covarianza

La volatilidad del portafolio **no** es el promedio ponderado de las volatilidades. Depende de
cómo se mueven los activos **entre sí**:

```text
σ²_p = wᵀ Σ w = Σᵢ Σⱼ wᵢ wⱼ cov(i, j)
```

```python
cov_anual = r.cov() * 252
vol_port = np.sqrt(pesos @ cov_anual @ pesos)     # 0.1788
```

```
         ACME    BETA    CIRC   DELTA
ACME   0.0726  0.0223  0.0463  0.0103
BETA   0.0223  0.0309  0.0284  0.0066
CIRC   0.0463  0.0284  0.1460  0.0113
DELTA  0.0103  0.0066  0.0113  0.0115
```

La diagonal tiene las varianzas (vol²) y el resto, las covarianzas. Con `@`, el álgebra de NumPy
del módulo 11 hace todo el trabajo.

## Diversificación

| | volatilidad anual |
|---|---|
| promedio ponderado de las 4 acciones | 0.2336 |
| portafolio con pesos iguales           | 0.1788 |

El portafolio tiene **23.5 % menos de riesgo** que el promedio de sus partes, sin resignar
retorno esperado. Es lo único "gratis" en finanzas: viene de que las correlaciones son menores
que 1, así que los movimientos se compensan en parte.

```python
beneficio = 1 - vol_port / (pesos @ vol_individual)
```

- Con correlación 1 (todo se mueve igual) no hay beneficio.
- Cuanto más bajas las correlaciones, mayor es el beneficio.
- Hay un piso: el **riesgo sistemático** (el del mercado, que afecta a todos) no se puede
  diversificar. Solo se elimina el riesgo **idiosincrático** de cada empresa.

## Buy & hold y la deriva de los pesos

Si comprás una vez y no tocás nada (**buy & hold**), los pesos **cambian solos**: lo que sube
pesa cada vez más.

```python
capital = 1000
acciones = capital * pesos / precios.iloc[0]          # cuántas acciones compré de cada uno
valor = (precios[activos] * acciones).sum(axis=1)     # valor diario: 1351.27 al final
pesos_finales = precios.iloc[-1] * acciones / valor.iloc[-1]
```

```
ACME 0.261   BETA 0.164   CIRC 0.289   DELTA 0.285
```

BETA bajó al 16 % y CIRC subió al 29 %: el portafolio ya **no es** el que elegiste, y su riesgo
cambió.

## Rebalanceo

**Rebalancear** es vender lo que subió y comprar lo que bajó para volver a los pesos objetivo.
El caso extremo es rebalancear **todos los días**, que equivale a aplicar pesos fijos a los
retornos:

```python
valor_rebal = capital * (1 + r @ pesos).cumprod()     # 1388.07 al final
```

En estos datos, el rebalanceo diario terminó arriba (1388 contra 1351), pero no es una regla: en
mercados con tendencia fuerte, buy & hold suele ganar, y en mercados que oscilan, el rebalanceo
"compra barato y vende caro". En la práctica se rebalancea cada mes, cada trimestre o cuando un
peso se desvía más de un umbral, porque **cada operación tiene costos** (lo vemos en
backtesting).

## Resumen

- Retorno del portafolio: `r @ pesos`. Retorno esperado anual: `pesos @ r.mean() * 252`.
- Volatilidad: `√(wᵀ Σ w)` con `Σ = r.cov() * 252`. No es el promedio de las volatilidades.
- Diversificar reduce el riesgo idiosincrático gracias a las correlaciones menores que 1.
- En buy & hold los pesos derivan; rebalancear los devuelve al objetivo.

## Ejercicio

Calculá el retorno, el retorno esperado y la volatilidad de un portafolio, el beneficio de
diversificación, el valor en buy & hold con los pesos finales y el valor con rebalanceo diario.

**Para profundizar:** H. Markowitz, *Portfolio Selection* (1952);
[Investopedia: Diversification](https://www.investopedia.com/terms/d/diversification.asp).
