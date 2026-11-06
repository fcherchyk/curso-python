# Backtesting: probar una estrategia sin engañarte

Un **backtest** simula cómo le habría ido a una regla de inversión con datos históricos. Es
fácil de programar y **todavía más fácil de hacer mal**: un backtest con errores siempre parece
excelente. Este capítulo arma uno simple y, sobre todo, muestra las trampas.

## La estrategia: cruce de medias móviles

Una regla clásica de seguimiento de tendencia:

- **Media corta** (20 días) por encima de la **media larga** (50 días): tendencia alcista,
  **comprado**.
- Si no: **afuera** (en efectivo).

```python
s = precios["ACME"]
corta = s.rolling(20).mean()
larga = s.rolling(50).mean()
senal = (corta > larga).astype(int)      # 1 = comprado, 0 = afuera
```

Los primeros 49 días la media larga es NaN, y `NaN > x` da `False`: la señal es 0 (afuera)
hasta tener datos suficientes.

## La trampa número uno: *look-ahead bias*

La señal del día `t` usa el precio de **cierre** del día `t`. Recién lo conocés cuando el día
terminó, así que **no podés haber operado durante ese día con esa información**. La posición
que realmente tenés el día `t` es la señal de **ayer**:

```python
posicion = senal.shift(1).fillna(0)      # operás al día siguiente de la señal
r = s.pct_change().fillna(0)
r_estrategia = posicion * r
```

Para ver cuánto engaña olvidarse del `shift`, probá una regla absurda: "estar comprado los días
que sube".

```python
trampa = (r > 0) * r                     # sin shift: sabe el futuro
honesta = (r > 0).shift(1).fillna(False) * r
```

En ACME, la versión con trampa multiplica el capital **214 veces** en tres años, y la honesta
gana un 8 %. Con medias móviles el error es menos obvio (58 % contra 56 %), y por eso es tan
peligroso: el resultado parece creíble.

## Costos de transacción

Cada vez que la posición cambia, pagás comisiones y el *spread* (la diferencia entre el precio
de compra y el de venta). Un modelo simple cobra un porcentaje por cada cambio:

```python
operaciones = posicion.diff().fillna(posicion).abs()   # 1 en cada entrada o salida
r_neta = posicion * r - 0.001 * operaciones            # 0.1 % por operación
```

`fillna(posicion)` cuenta la primera entrada si la posición arranca en 1. Una estrategia que
opera mucho puede pasar de ganadora a perdedora solo por los costos.

## Comparar contra buy & hold

Una estrategia solo vale si le gana a la alternativa más simple: **comprar y no hacer nada**.

| ACME (2023–2025) | retorno total | operaciones | tiempo comprado |
|---|---|---|---|
| Buy & hold                         | 41.2 % | 1  | 100 % |
| Cruce 20/50 sin costos             | 55.6 % | 15 | 54 % |
| Cruce 20/50 con 0.1 % por operación | 53.3 % | 15 | 54 % |

En ACME la estrategia ganó. En el INDICE, la misma regla rinde **22 %** contra **30 %** de buy &
hold: **perdió**. Un resultado en un solo activo y un solo período no prueba nada.

## La curva de capital (*equity curve*)

```python
equity = capital * (1 + r_neta).cumprod()
buy_hold = capital * (1 + r).cumprod()
fig, ax = plt.subplots()
ax.plot(equity, label="Estrategia")
ax.plot(buy_hold, label="Buy & hold")
```

Mirá la curva entera, no solo el número final: ¿cuándo ganó?, ¿cuánto tiempo estuvo debajo de su
máximo (drawdown, capítulo 2)?

## Otras trampas

- **Sobreajuste (*overfitting*)**: probar 100 combinaciones de medias y quedarse con la mejor
  encuentra ruido, no una señal. Separá los datos: optimizá en un período y validá en otro que
  no hayas mirado (*out-of-sample*).
- **Sesgo de supervivencia**: si solo testeás con empresas que hoy existen, te salteás las que
  quebraron.
- **Ejecución irreal**: suponer que operás exactamente al cierre, sin impacto en el precio.
- **Datos sintéticos**: estos precios son un random walk. Por construcción, **ninguna**
  estrategia tiene ventaja real en ellos; cualquier "ganancia" es suerte. Lo mismo te puede
  pasar con datos reales sin darte cuenta.

Herramientas como `vectorbt` o `backtrader` resuelven la mecánica, pero no estos sesgos: esos
siempre los tenés que cuidar vos.

## Resumen

- Señal con datos hasta `t` → posición en `t + 1`: `senal.shift(1)`. Sin shift, el backtest
  hace trampa.
- Retorno de la estrategia: `posicion * r - costo * |Δposicion|`.
- Compará siempre contra buy & hold, en varios activos y períodos.
- Desconfiá de los backtests demasiado buenos: overfitting, supervivencia y ejecución irreal.

## Ejercicio

Implementá la señal de cruce, la posición sin look-ahead, los retornos netos de costos, un
resumen comparado con buy & hold y la equity curve.

**Para profundizar:** M. López de Prado, *Advances in Financial Machine Learning*, cap. 11
("The Dangers of Backtesting"); [vectorbt](https://vectorbt.dev/).
