# groupby: grouping and aggregating

"How much did each branch sell?", "What's the average ticket per category?", "What share does
each sale have within its branch?" Almost every business question is an **aggregation by
groups**. In pandas you answer it with `groupby`, which follows the **split-apply-combine**
pattern: split the rows into groups, apply an operation to each group and combine the results.

## The basics

```python
sales.groupby("branch")["total"].sum()
# branch
# Central    230900
# North      245400
# South      380300
# Name: total, dtype: int64

sales.groupby("branch")["total"].agg(["sum", "mean", "count"])
sales.groupby(["branch", "category"])["quantity"].sum()   # several keys → MultiIndex
sales.groupby("branch").size()             # number of rows per group
```

- The group keys become the **index** of the result. With `as_index=False`, or with
  `.reset_index()`, they stay as columns.
- Common aggregations: `sum`, `mean`, `median`, `count` (non-null), `size` (rows), `min`, `max`,
  `std`, `nunique`, `first` and `last`.
- It's the direct equivalent of SQL's `GROUP BY`.

## Named aggregations: the recommended style

```python
summary = sales.groupby("category").agg(
    units=("quantity", "sum"),
    revenue=("total", "sum"),
    average_ticket=("total", "mean"),
    distinct_products=("product", "nunique"),
).sort_values("revenue", ascending=False)
```

Each argument is `output_name=(column, function)`. The result has clearly named columns instead
of a hard-to-handle column MultiIndex. The function can also be your own:
`("total", lambda s: s.quantile(0.9))`.

## `transform`: the group's result, on every row

`agg` **reduces** each group to one row. `transform` returns a value **for each original row**,
aligned with the DataFrame. It's what you need to compare each row with its group:

```python
branch_total = sales.groupby("branch")["total"].transform("sum")
sales["share"] = sales["total"] / branch_total

# Deviation from the category average
sales["vs_average"] = sales["total"] - sales.groupby("category")["total"].transform("mean")
```

Without `transform`, you'd have to aggregate, merge the result back onto the rows and then
divide.

## `filter` and `apply`

```python
# Only the groups (branches) with more than 20 sales
sales.groupby("branch").filter(lambda g: len(g) > 20)

# apply: an arbitrary function per group (flexible but slower)
sales.groupby("branch").apply(lambda g: g.nlargest(2, "total"))
```

Prefer `agg`/`transform` with named functions (`"sum"`, `"mean"`): they're optimized. Use `apply`
only when there's no alternative.

## "The largest in each group"

A very common pattern: the best-selling product **in each** branch.

```python
units = sales.groupby(["branch", "product"])["quantity"].sum()
idx = units.groupby(level="branch").idxmax()      # (branch, product) of the maximum
units.loc[idx]
```

Another way: `sort_values` + `groupby(...).head(1)`, or `.nlargest(1)` within the group.

## Pivot tables: `pivot_table`

The spreadsheet pivot table:

```python
pd.pivot_table(
    sales,
    values="total",
    index="branch",            # rows
    columns="category",        # columns
    aggfunc="sum",
    fill_value=0,
    margins=True,              # row and column totals ("All")
)
```

`pd.crosstab(sales["branch"], sales["category"])` counts frequencies, and
`.unstack()`/`.stack()` move an index level to columns and back.

## Grouping by time

With dates you can group by period:

```python
sales.groupby(sales["date"].dt.month)["total"].sum()
sales.groupby(pd.Grouper(key="date", freq="ME"))["total"].sum()    # by month end
```

We'll see this with `resample` in the time series chapter.

## Summary

- `groupby(key)[col].agg(...)`: split-apply-combine, like SQL's `GROUP BY`.
- Named aggregations: `agg(output=("column", "function"))`.
- `transform` returns a value per row (shares, deviations from the group).
- `filter` to discard groups; `apply` only as a last resort.
- The largest per group: `groupby(...).idxmax()` or `sort_values` + `head(1)`.
- `pivot_table` for cross tabulations.

## Exercise

On the sales data: totals per branch, a per-category summary with named aggregations, each
sale's share within its branch, a pivot table and the top product in each branch.

**Further reading:** [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html),
[Reshaping and pivot tables](https://pandas.pydata.org/docs/user_guide/reshaping.html).
