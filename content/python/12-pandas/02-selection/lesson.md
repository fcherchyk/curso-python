# Selecting and filtering: loc, iloc, masks and copy-on-write

Picking rows and columns is what you'll do most with pandas, and also where the most confusion
lives: `[]`, `loc` and `iloc` look alike but aren't the same, and modifying a subset of the data
used to trigger the infamous `SettingWithCopyWarning`. In pandas 3 the rule became simple thanks
to **copy-on-write**. In this chapter we build a clear mental model.

## `loc`: by labels

```python
df.loc[5]                         # the row with index 5 → Series
df.loc[5, "product"]              # a single value
df.loc[[1, 5, 9], ["product", "total"]]      # rows and columns by label
df.loc[10:20]                     # INCLUDES 20! (label slices are inclusive)
df.loc[:, "date":"product"]       # a range of columns, also inclusive
```

## `iloc`: by positions

```python
df.iloc[0]                        # the first row, whatever its label
df.iloc[0, 2]                     # row 0, column 2
df.iloc[:5]                       # the first 5 (excludes 5, like Python)
df.iloc[-3:, [0, 1]]              # the last 3 rows, columns 0 and 1
```

**Rule:** `loc` = labels (inclusive), `iloc` = positions (exclusive, like Python). If the index
is 0, 1, 2… they look the same, but after filtering or sorting they stop matching:

```python
ordered = df.sort_values("total", ascending=False)
ordered.loc[0]      # the row with LABEL 0, wherever it is
ordered.iloc[0]     # the FIRST row: the one with the largest total
```

## Filtering with boolean masks

Same as in NumPy, but the columns have names:

```python
df[df["total"] > 10_000]
df[(df["branch"] == "Central") & (df["quantity"] >= 5)]       # & | ~ with parentheses
df[df["product"].isin(["cocoa", "mug"])]
df[df["date"].between("2025-02-01", "2025-02-28")]
df.loc[df["total"] > 10_000, ["product", "total"]]   # filter AND pick columns
```

### `query`: the same filter as text

```python
df.query("total > 10_000 and branch == 'Central'")
minimum = 5
df.query("quantity >= @minimum")         # @ to use Python variables
```

`query` reads well for long filters. It works on columns by name (names with spaces go between
backticks).

## Copy-on-write: the pandas 3 rule

**Every result of a selection behaves like a copy.** Modifying it never changes the original
DataFrame:

```python
central = df[df["branch"] == "Central"]
central["total"] = 0              # modifies `central`, NOT `df` (and no warnings)
```

To modify the **original**, do it in **a single step**, with `loc` on the DataFrame itself:

```python
df.loc[df["branch"] == "Central", "total"] = 0        # ✓ modifies df
df["total"][df["branch"] == "Central"] = 0            # ✗ chained assignment: does NOTHING
                                                       #   (pandas 3 raises ChainedAssignmentError)
```

Internally, pandas shares the data and only copies when someone writes, which is why it's called
*copy-on-write*. That makes it efficient.

> In pandas 1.x and 2.x the behavior depended on whether the result was a "view" or a "copy",
> and that's where `SettingWithCopyWarning` came from. In old code and tutorials you'll see
> `.copy()` everywhere "just in case": in pandas 3 you no longer need it.

## Functions that don't mutate

A good habit in data analysis is to write functions that **take a DataFrame and return another
one**, without modifying the input. That way notebook cells can be re-run and the steps chain
together:

```python
def with_discount(df: pd.DataFrame, category: str, pct: float) -> pd.DataFrame:
    result = df.copy()            # explicit: we're about to write
    mask = result["category"] == category
    result.loc[mask, "unit_price"] *= 1 - pct
    return result
```

Or with `assign`, which always returns a new DataFrame:

```python
df.assign(total=lambda d: d["quantity"] * d["unit_price"])
```

## Picking columns

```python
df[["a", "b"]]
df.drop(columns=["c"])
df.filter(like="price")               # columns whose name contains "price"
df.select_dtypes("number")            # numeric columns only
df.rename(columns={"qty": "quantity"})
```

## Summary

- `loc` by labels (inclusive); `iloc` by positions (exclusive).
- Masks with `&`, `|` and `~` in parentheses; `isin` and `between`; `query` for readable filters.
- Copy-on-write: a selection never modifies the original; to write, `df.loc[mask, col] = v`
  in one step; never chained assignment.
- Analysis functions take and return DataFrames without mutating the input (`copy()` or `assign`).

## Exercise

Filters with combined conditions, `query` with variables, the difference between `loc` and
`iloc` after sorting, and a function that applies a discount without modifying the original
DataFrame.

**Further reading:** [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html),
[Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html).
