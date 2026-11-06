# Limpieza de datos

Los datos reales vienen sucios: espacios de más, mayúsculas inconsistentes, números guardados
como texto con formato local, celdas vacías, duplicados y fechas en mil formatos. Se suele decir
que el 80 % del trabajo con datos es limpiarlos. pandas tiene herramientas vectorizadas para
cada uno de esos problemas, y la clave es aplicarlas en un **pipeline reproducible**, no a mano.

## Diagnóstico primero

```python
df.info()                       # tipos y cantidad de no nulos por columna
df.isna().sum()                 # nulos por columna
df.duplicated().sum()           # filas duplicadas exactas
df["ciudad"].value_counts(dropna=False)   # ver las variantes ("Rosario", "rosario", NaN…)
df.describe(include="all")
```

Antes de limpiar, **mirá** los valores: `value_counts` sobre una columna de texto suele revelar
de inmediato las inconsistencias.

## Texto: el accessor `.str`

Las operaciones de strings vectorizadas viven en `serie.str`:

```python
s.str.strip()                     # espacios al principio y al final
s.str.lower(), s.str.upper(), s.str.title()
s.str.replace(r"\s+", " ", regex=True)       # colapsar espacios internos
s.str.contains("mail", case=False)
s.str.startswith("A"), s.str.len()
s.str.split("@").str[1]           # el dominio de un email
s.str.extract(r"(\d+)")           # grupos de una regex → columnas
```

Los nulos se mantienen como nulos (no rompen como en un bucle con `.strip()` sobre `None`).

## Números como texto

```python
pd.to_numeric(s, errors="coerce")       # lo que no se puede convertir → NaN
```

Con `errors="coerce"`, `"sin dato"` pasa a `NaN` en lugar de cortar todo el proceso con una
excepción. Para formatos locales (`"$ 1.234,50"`), primero se limpia con `.str`:

```python
montos = (
    s.str.replace("$", "", regex=False)
     .str.replace(".", "", regex=False)      # separador de miles
     .str.replace(",", ".", regex=False)     # coma decimal → punto
     .str.strip()
)
pd.to_numeric(montos, errors="coerce")
```

Si lo leés directo de un CSV, `pd.read_csv(..., thousands=".", decimal=",")` resuelve buena
parte.

## Nulos: detectar, eliminar o completar

```python
df.isna(), df.notna()
df.dropna(subset=["email"])             # descartar filas sin email
df["ciudad"].fillna("Desconocida")
df["edad"].fillna(df["edad"].median())
df.ffill()                              # propagar el último valor válido (series de tiempo)
```

Decidí **por columna** y con criterio de negocio: ¿un email faltante invalida al cliente? ¿Una
edad faltante se puede estimar o mejor dejarla vacía? No hay una regla única.

### Enteros con nulos: `Int64`

Un `int64` no puede tener `NaN`, así que una columna de enteros con un nulo se convierte en
`float64`: 31 pasa a ser 31.0. El dtype **`Int64`** (con mayúscula) es un entero que admite nulos
(`pd.NA`):

```python
pd.to_numeric(df["edad"], errors="coerce").astype("Int64")
```

## Duplicados

```python
df.drop_duplicates()                              # filas idénticas
df.drop_duplicates(subset=["email"], keep="first")  # mismo email = misma persona
```

Normalizá **antes** de deduplicar: `"ANA@mail.com"` y `"ana@mail.com "` son la misma persona,
pero no son strings iguales hasta que limpiás mayúsculas y espacios.

## Fechas

```python
pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
pd.to_datetime(s, dayfirst=True)        # 03/04 = 3 de abril
s.dt.year, s.dt.month, s.dt.day_name()
```

Indicar el `format` explícito es más rápido y evita ambigüedades (¿03/04 es marzo o abril?).

## Columnas derivadas: `assign` y pipelines con `pipe`

```python
limpio = (
    crudo
    .assign(
        email=lambda d: d["email"].str.strip().str.lower(),
        nombre=lambda d: d["nombre"].str.strip().str.title(),
    )
    .dropna(subset=["email"])
    .drop_duplicates(subset=["email"])
    .pipe(convertir_montos, columna="saldo")    # tus funciones en la cadena
    .reset_index(drop=True)
)
```

Encadenar métodos (*method chaining*) deja el proceso **legible de arriba hacia abajo**, sin
variables intermedias, y cada paso devuelve un DataFrame nuevo. Es el estilo idiomático del
pandas moderno.

## Resumen

- Diagnóstico: `info`, `isna().sum()`, `duplicated` y `value_counts(dropna=False)`.
- Texto con `.str` (strip, lower, title, replace con regex, split).
- `pd.to_numeric`/`to_datetime` con `errors="coerce"`; los formatos locales se limpian antes.
- Nulos: `dropna(subset=...)` / `fillna` con criterio; `Int64` para enteros con nulos.
- Normalizar antes de `drop_duplicates(subset=...)`.
- Pipelines con `assign` y `pipe`.

## Ejercicio

El archivo `clientes.csv` tiene todos los problemas de este capítulo. Escribí las funciones
de limpieza y el pipeline final.

```
nombre,email,edad,saldo,ciudad
  ana PÉREZ,ANA@mail.com,31,"$ 1.234,50",Rosario
Beto gómez ,beto@mail.com ,27,"$ 100,00",rosario
caro díaz,caro@mail.com,sin dato,,Córdoba
ana pérez,ana@mail.com,31,"$ 1.234,50",Rosario
...
```

**Para profundizar:** [Working with text data](https://pandas.pydata.org/docs/user_guide/text.html),
[Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html).
