# Combining tables: merge, join and concat

Data almost never comes in a single table: sales in one place, the product catalog in another,
each month in a separate file. pandas combines tables in two ways: **by key** (`merge`, SQL's
`JOIN`) and **by stacking** (`concat`, the `UNION`). The hard part isn't the syntax, it's **not
losing or duplicating rows without noticing**, and for that pandas has validation tools you
should always use.

## `merge`: joining on key columns

```python
sales.merge(products, on="product", how="left")
```

| `how`     | Which rows remain                                        | SQL                 |
|-----------|----------------------------------------------------------|---------------------|
| `"inner"` | only those with a key in **both** tables (default)       | `INNER JOIN`        |
| `"left"`  | **all** rows from the left; no match → NaN               | `LEFT JOIN`         |
| `"right"` | all rows from the right                                  | `RIGHT JOIN`        |
| `"outer"` | all rows from both                                       | `FULL OUTER JOIN`   |
| `"cross"` | Cartesian product                                        | `CROSS JOIN`        |

To enrich a fact table (sales) with attributes (the catalog), the usual choice is **`left`**: you
don't want to lose sales because a product is missing from the catalog.

```python
# Keys with different names
orders.merge(customers, left_on="customer_id", right_on="id", suffixes=("", "_customer"))
# Several keys
a.merge(b, on=["branch", "date"])
```

## The traps: rows that get lost or multiplied

1. **With `inner`, you silently lose rows** if some key isn't in the other table.
2. **If the key repeats in the right table, the left rows get multiplied.** A product duplicated
   in the catalog duplicates all its sales, and the totals come out inflated without any error.

### `validate`: let pandas check your assumptions

```python
sales.merge(products, on="product", how="left", validate="many_to_one")
```

With `validate`, pandas **raises `MergeError`** if the relationship isn't the one you declared:
`"one_to_one"`, `"one_to_many"`, `"many_to_one"` or `"many_to_many"`. It's one line that saves
you hours of hunting for why the numbers don't add up. Always use it.

### `indicator`: where did each row come from?

```python
r = sales.merge(products, on="product", how="left", indicator=True)
r["_merge"].value_counts()      # both / left_only / right_only
r.loc[r["_merge"] == "left_only", "product"].unique()   # sales with no product in the catalog
```

It's the idiomatic way to find "orphan" keys (the *anti-join*).

### Check before and after

```python
assert products["product"].is_unique                      # the key is unique
assert len(result) == len(sales)                           # a many-to-one left join adds no rows
```

## `join`: merge on the index

```python
sales.join(products.set_index("product"), on="product")
df1.join(df2)                   # index against index
```

It's a shortcut for `merge` when the right-hand key is its index.

## `concat`: stacking

```python
january = pd.read_csv("sales_2025_01.csv")
february = pd.read_csv("sales_2025_02.csv")

pd.concat([january, february], ignore_index=True)       # one below the other
pd.concat({"jan": january, "feb": february})            # with an index level that marks the source
pd.concat([a, b], axis=1)                               # side by side (aligning on the index)
```

- `ignore_index=True` renumbers the index (otherwise you get repeated index values).
- Passing a **dict** adds a source label, which becomes a column with `.reset_index(level=0)`.
- If the columns don't match, the missing ones are filled with `NaN`.
- **Don't `concat` inside a loop** (it's quadratic): collect the DataFrames in a list and
  concatenate once.

```python
parts = [pd.read_csv(path) for path in sorted(Path("data").glob("sales_*.csv"))]
everything = pd.concat(parts, ignore_index=True)
```

## Summary

- `merge(on=..., how=...)`: `left` to enrich without losing rows.
- **Always** `validate="many_to_one"` (or whatever relationship applies) to catch duplicate
  keys.
- `indicator=True` to find rows with no match.
- `join` when the key is the index.
- `concat` to stack (with `ignore_index` or a dict for the source); collect in a list and
  concatenate once.

## Exercise

`sales.csv` (id, date, branch, product, quantity) and `products.csv` (product, category,
unit_price). The catalog **is missing a product** that does appear in the sales.

**Further reading:** [Merge, join, concatenate and compare](https://pandas.pydata.org/docs/user_guide/merging.html).
