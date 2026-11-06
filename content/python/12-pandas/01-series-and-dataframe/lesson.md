# Series and DataFrame

pandas is **the** Python tool for tabular data: CSV, Excel, database tables, logs and time
series. It adds two fundamental things to NumPy: **labels** (named rows and columns, not just
positions) and **a different type per column** (dates, text, numbers and categories in the same
table). If you've ever built a spreadsheet with formulas, pandas is the same idea, but
programmable, reproducible and able to handle millions of rows.

```bash
uv add pandas
```
```python
import pandas as pd       # the universal alias
```

## Series: a column with an index

```python
prices = pd.Series([3500, 9800, 1200], index=["cocoa", "coffee", "tea"], name="price")
prices["coffee"]          # 9800: access by label
prices.iloc[0]            # 3500: access by position
prices * 1.21             # vectorized, like NumPy
prices[prices > 2000]     # masks, like NumPy
prices.index              # Index(['cocoa', 'coffee', 'tea'])
prices.values             # the underlying NumPy array (better: .to_numpy())
pd.Series({"a": 1, "b": 2})   # from a dict: the keys become the index
```

A Series is a NumPy array **with an index**. Operations between Series **align by label**, not
by position:

```python
a = pd.Series({"x": 1, "y": 2})
b = pd.Series({"y": 10, "z": 20})
a + b        # x: NaN, y: 12.0, z: NaN  ← aligned by label; where one is missing, NaN
```

## DataFrame: a table

A DataFrame is a collection of Series that **share the index**: each column is a Series.

```python
df = pd.DataFrame({
    "product": ["cocoa", "coffee", "tea"],
    "price": [3500, 9800, 1200],
    "stock": [10, 0, 25],
})

df["price"]                # one column → Series
df[["product", "stock"]]   # several columns → DataFrame (double brackets!)
df["total"] = df["price"] * df["stock"]       # new column, vectorized
df.shape                   # (3, 4)
df.columns, df.index, df.dtypes
len(df)
```

Other ways to create one:

```python
pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])   # list of dicts (records)
pd.DataFrame(matrix, columns=["x", "y"])             # from NumPy
```

## Reading data

```python
df = pd.read_csv("sales.csv")
df = pd.read_csv("sales.csv", parse_dates=["date"], index_col="id")
df = pd.read_csv("data.csv", sep=";", decimal=",", encoding="latin-1")   # European format
pd.read_excel("file.xlsx", sheet_name="Sheet1")        # needs openpyxl
pd.read_json(...), pd.read_parquet(...), pd.read_sql(query, connection)
df.to_csv("output.csv", index=False), df.to_parquet("output.parquet")
```

- `parse_dates` converts columns to dates (`datetime64`); without it, they stay as text.
- `index_col` uses a column as the index.
- **Parquet** is the recommended format for storing intermediate data: fast, compressed, and it
  preserves the types.

## Exploring

```python
df.head(), df.tail(3), df.sample(5)
df.info()              # columns, types, non-null counts and memory
df.describe()          # statistics for the numeric columns
df["branch"].value_counts()        # frequency of each value
df["branch"].unique(), df["branch"].nunique()
df.sort_values("total", ascending=False).head(10)
df["total"].sum(), df["total"].mean(), df["total"].idxmax()
```

`idxmax()` returns the **label** (not the position) of the maximum: it's pandas' `argmax`.

## dtypes in pandas 3

| Data                  | dtype                                    |
|-----------------------|------------------------------------------|
| integers              | `int64` (or `Int64` if it allows nulls)  |
| decimals              | `float64`                                |
| text                  | `str` (pandas 3's string dtype)          |
| dates                 | `datetime64[ns]`                         |
| true/false            | `bool` (or `boolean` with nulls)         |
| few repeated values   | `category` (saves memory)                |

`df.astype({"stock": "int32"})` converts, and `pd.to_datetime`/`pd.to_numeric` are the "robust"
conversions (we'll see them in the cleaning chapter).

> **pandas 3 (2026)** changed two important things compared to pandas 1.x and 2.x, which is
> what you'll see in many tutorials: **copy-on-write** is always on (next chapter), and text has
> its own `str` dtype instead of `object`.

## Summary

- Series = array with an index; DataFrame = columns (Series) sharing the index.
- Operations align by label; where there's no match, `NaN`.
- `df["col"]` gives a Series, `df[["a", "b"]]` a DataFrame, and `df["new"] = ...` adds columns.
- `read_csv` with `parse_dates` and `index_col`; Parquet for storage.
- `head`, `info`, `describe`, `value_counts`, `sort_values` and `idxmax` for exploring.

## Exercise

Create Series and DataFrames, read the sales CSV with the right types, add a computed column and
build a summary. The file `sales.csv` has the columns `id, date, branch, product, quantity,
category, unit_price`.

**Further reading:** [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html),
[IO tools](https://pandas.pydata.org/docs/user_guide/io.html).
