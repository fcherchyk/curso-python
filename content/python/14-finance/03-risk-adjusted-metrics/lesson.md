# Métricas ajustadas por riesgo: Sharpe, Sortino, correlación y beta

CIRC rindió un 15 % anual y DELTA, también un 15 %. ¿Son igual de buenas? No: CIRC lo logró con
38 % de volatilidad y una caída del 51 %, y DELTA con 11 % de volatilidad y una caída del 12 %.
Las métricas ajustadas por riesgo responden a la pregunta: **¿cuánto retorno obtengo por cada
unidad de riesgo?**

## La tasa libre de riesgo

Antes que nada: invertir en algo riesgoso solo tiene sentido si paga **más** que la alternativa
sin riesgo (bonos del Tesoro de corto plazo de EE. UU., por ejemplo). Lo que importa es el
**exceso de retorno** sobre esa tasa. Usamos un 4 % anual, que en datos diarios es:

```python
rf_diaria = 0.04 / 252
exceso = retornos - rf_diaria
```

## Ratio de Sharpe

```text
Sharpe = media(exceso diario) / desvío(retornos diarios) × √252
```

Es el exceso de retorno por unidad de volatilidad, anualizado. La media escala con 252 y el
desvío con √252, así que el cociente escala con 252 / √252 = √252. Por convención, el Sharpe
usa la media **aritmética** de los retornos (a diferencia del retorno anualizado compuesto del
capítulo 1).

```
ACME 0.40   BETA −0.36   CIRC 0.46   DELTA 0.98   INDICE 0.36
```

DELTA tiene un Sharpe de casi el doble que CIRC: el mismo retorno con mucho menos riesgo. Como
referencia, un Sharpe mayor que 1 sostenido en el tiempo es muy bueno, y uno negativo significa
que habría convenido la tasa libre de riesgo.

## Ratio de Sortino

El Sharpe castiga la volatilidad **hacia arriba** igual que la volatilidad hacia abajo, pero a
nadie le molestan las subas. El Sortino solo usa el **desvío a la baja** (*downside deviation*):

```python
abajo = exceso.clip(upper=0)                          # los excesos positivos cuentan como 0
desvio_abajo = np.sqrt((abajo ** 2).mean()) * np.sqrt(252)
sortino = exceso.mean() * 252 / desvio_abajo
```

```
ACME 0.58   BETA −0.49   CIRC 0.69   DELTA 1.46   INDICE 0.52
```

Ojo: el desvío a la baja se calcula sobre **todos** los días (con 0 en los positivos), no
solo sobre los negativos.

## Correlación

```python
r.corr()
```

```
        ACME  BETA  CIRC  DELTA  INDICE
ACME    1.00  0.47  0.45   0.36    0.69
DELTA   0.36  0.35  0.28   1.00    0.45
```

Mide si dos activos **se mueven juntos** (+1), en direcciones opuestas (−1) o de forma
independiente (0). Es la clave de la diversificación del próximo capítulo: combinar activos
**poco correlacionados** reduce el riesgo del conjunto. DELTA es el activo menos correlacionado
con los demás.

Cuidado: la correlación **cambia con el tiempo**, y en las crisis tiende a subir. Justo cuando
más la necesitás, la diversificación funciona peor.

## Beta

La beta mide **cuánto se mueve un activo cuando se mueve el mercado**:

```text
β = cov(r_activo, r_mercado) / var(r_mercado)
```

```python
beta = r["ACME"].cov(r["INDICE"]) / r["INDICE"].var()     # 1.16
```

```
ACME 1.16   BETA 0.78   CIRC 1.46   DELTA 0.30
```

- β = 1: se mueve igual que el mercado. β > 1 amplifica (CIRC: si el índice cae 10 %, se espera
  que caiga 14.6 %); β < 1 amortigua.
- La beta es la pendiente de la regresión de los retornos del activo contra los del mercado. Es
  el corazón del **CAPM**, que dice que el retorno esperado depende solo del riesgo de mercado
  (beta), porque el resto del riesgo se elimina diversificando.
- Lo que el activo rinde por encima de lo que predice su beta se llama **alfa**.

## Resumen

- Trabajá con el **exceso** sobre la tasa libre de riesgo.
- Sharpe: `exceso.mean() / r.std() * √252`. Sortino: igual, pero dividiendo solo por el desvío
  a la baja.
- `corr()` para ver qué se mueve junto; las correlaciones bajas son las que diversifican.
- Beta = cov / var del mercado: sensibilidad al mercado.

## Ejercicio

Implementá Sharpe, Sortino, beta contra el índice y una función que encuentre el activo menos
correlacionado con uno dado.

**Para profundizar:** W. Sharpe, *The Sharpe Ratio* (1994);
[Investopedia: Sortino Ratio](https://www.investopedia.com/terms/s/sortinoratio.asp).
