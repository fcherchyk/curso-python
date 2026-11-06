# Series de tiempo

Precios, ventas diarias, métricas de un servidor, sensores: muchos datos tienen una **fecha** como
eje principal. pandas nació en un fondo de inversión precisamente para esto, y tiene
herramientas de primera para series de tiempo: un índice de fechas que se puede rebanar por
período, cambio de frecuencia (`resample`), ventanas móviles (`rolling`), desplazamientos
(`shift`) y variaciones (`pct_change`). Es la base del módulo de finanzas.

## El `DatetimeIndex`

```python
precios = pd.read_csv("precios.csv", index_col="fecha", parse_dates=True)
precios.index            # DatetimeIndex(['2023-01-02', ...], dtype='datetime64[ns]')
precios.index.min(), precios.index.max()
```

Con un índice de fechas, rebanar es muy natural:

```python
precios.loc["2024"]                       # todo 2024
precios.loc["2024-03"]                    # marzo de 2024
precios.loc["2024-03-01":"2024-06-30"]    # un rango (inclusivo)
precios.loc[precios.index.dayofweek == 0] # solo los lunes
```

Atributos útiles: `.year`, `.month`, `.day`, `.dayofweek`, `.quarter` y `.is_month_end` (en una
columna de fechas se accede con `.dt`, por ejemplo `df["fecha"].dt.month`).

## Cambiar la frecuencia: `resample`

`resample` es un `groupby` por períodos de tiempo:

```python
precios.resample("ME").last()        # el último precio de cada mes (ME = month end)
precios.resample("W").mean()         # promedio semanal
ventas.resample("D").sum()           # total diario
precios.resample("YE").agg(["first", "last", "max"])
```

Frecuencias habituales: `"D"` (día), `"B"` (día hábil), `"W"` (semana), `"ME"` (fin de mes),
`"QE"` (fin de trimestre) y `"YE"` (fin de año). Para precios de cierre, el valor representativo
del período es el **último** (`last()`), no el promedio.

## Desplazar: `shift`

```python
precios["ACME"].shift(1)        # el valor del día ANTERIOR, alineado con hoy
precios["ACME"].shift(-1)       # el del día siguiente (¡cuidado: es mirar el futuro!)
```

`shift` mueve los datos y mantiene el índice: en cada fecha queda el valor de la fecha anterior.
Es la herramienta para comparar con "ayer" y, en finanzas, para **evitar usar información que
todavía no existía** (el *look-ahead bias*, lo vemos en backtesting).

## Variaciones: `pct_change` y `diff`

```python
precios.pct_change()            # (hoy / ayer) - 1  ← retornos diarios
precios.diff()                  # hoy - ayer
precios.pct_change(periods=5)   # contra hace 5 días
(1 + retornos).cumprod()        # retorno acumulado: crecimiento de 1 peso invertido
```

`pct_change()` es exactamente `precios / precios.shift(1) - 1`. La primera fila queda `NaN`
porque no hay día anterior; se descarta con `.dropna()`.

## Ventanas móviles: `rolling`

```python
precios["ACME"].rolling(20).mean()      # media móvil de 20 días
retornos.rolling(60).std()              # volatilidad móvil
precios.rolling("30D").max()            # ventana por TIEMPO (30 días calendario)
precios.expanding().max()               # máximo histórico hasta cada fecha
```

Las primeras `ventana - 1` filas quedan en `NaN`, porque todavía no hay datos suficientes (se
puede cambiar con `min_periods`). `expanding()` es una ventana que va creciendo: útil para
"máximo hasta hoy" o drawdowns.

## Combinar herramientas: cruces de medias móviles

"¿En qué días la media corta cruzó por **encima** de la larga?"

```python
corta = precio.rolling(20).mean()
larga = precio.rolling(50).mean()
arriba = corta > larga
cruce = arriba & ~arriba.shift(1, fill_value=False)    # hoy arriba y ayer no
precio.index[cruce]
```

Comparar una condición con su propio `shift` detecta **cambios de estado**. Es un patrón que vas a
reutilizar mucho.

## Zonas horarias

```python
idx.tz_localize("UTC").tz_convert("America/Argentina/Buenos_Aires")
```

Igual que con `datetime`: guardá en UTC y convertí para mostrar.

## Resumen

- `read_csv(..., index_col="fecha", parse_dates=True)` da un `DatetimeIndex`; `loc["2024-03"]`
  rebana por período.
- `resample("ME").last()` y compañía para cambiar la frecuencia.
- `shift` para comparar con el pasado; `pct_change`/`diff` para las variaciones; `cumprod` para
  acumular.
- `rolling(n)` para ventanas móviles; `expanding()` para acumulados históricos.
- Condición + `shift` para detectar cambios de estado (cruces).

## Ejercicio

Sobre `precios.csv` (precios diarios de ACME, BETA, CIRC, DELTA y un INDICE, de 2023 a 2025):
cierres mensuales, retornos, medias móviles, rendimiento por año y los cruces alcistas de medias.

**Para profundizar:** [Time series / date functionality](https://pandas.pydata.org/docs/user_guide/timeseries.html),
[Windowing operations](https://pandas.pydata.org/docs/user_guide/window.html).
