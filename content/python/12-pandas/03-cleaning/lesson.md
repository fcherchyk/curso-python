# Data cleaning

Real data comes in dirty: extra spaces, inconsistent capitalization, numbers stored as text in a
local format, empty cells, duplicates and dates in a thousand formats. People often say that
80 % of working with data is cleaning it. pandas has vectorized tools for each of those
problems, and the key is to apply them in a **reproducible pipeline**, not by hand.

## Diagnose first

```python
df.info()                       # types and non-null count per column
df.isna().sum()                 # nulls per column
df.duplicated().sum()           # exact duplicate rows
df["city"].value_counts(dropna=False)    # see the variants ("Boston", "boston", NaN…)
df.describe(include="all")
```

Before cleaning, **look** at the values: `value_counts` on a text column usually reveals the
inconsistencies right away.

## Text: the `.str` accessor

Vectorized string operations live in `series.str`:

```python
s.str.strip()                     # spaces at the start and end
s.str.lower(), s.str.upper(), s.str.title()
s.str.replace(r"\s+", " ", regex=True)       # collapse inner spaces
s.str.contains("mail", case=False)
s.str.startswith("A"), s.str.len()
s.str.split("@").str[1]           # the domain of an email
s.str.extract(r"(\d+)")           # regex groups → columns
```

Nulls stay null (they don't blow up the way calling `.strip()` on `None` in a loop does).

## Numbers as text

```python
pd.to_numeric(s, errors="coerce")       # whatever can't be converted → NaN
```

With `errors="coerce"`, `"unknown"` becomes `NaN` instead of stopping the whole process with an
exception. For local formats (`"$ 1.234,50"`, European style), clean with `.str` first:

```python
amounts = (
    s.str.replace("$", "", regex=False)
     .str.replace(".", "", regex=False)      # thousands separator
     .str.replace(",", ".", regex=False)     # decimal comma → dot
     .str.strip()
)
pd.to_numeric(amounts, errors="coerce")
```

If you're reading straight from a CSV, `pd.read_csv(..., thousands=".", decimal=",")` handles
much of it.

## Nulls: detect, drop or fill

```python
df.isna(), df.notna()
df.dropna(subset=["email"])             # drop rows without an email
df["city"].fillna("Unknown")
df["age"].fillna(df["age"].median())
df.ffill()                              # carry the last valid value forward (time series)
```

Decide **per column** and with business judgment: does a missing email invalidate the customer?
Can a missing age be estimated, or is it better left empty? There's no single rule.

### Integers with nulls: `Int64`

An `int64` can't hold `NaN`, so an integer column with one null becomes `float64`: 31 turns into
31.0. The **`Int64`** dtype (capitalized) is an integer that allows nulls (`pd.NA`):

```python
pd.to_numeric(df["age"], errors="coerce").astype("Int64")
```

## Duplicates

```python
df.drop_duplicates()                              # identical rows
df.drop_duplicates(subset=["email"], keep="first")  # same email = same person
```

Normalize **before** deduplicating: `"ALICE@mail.com"` and `"alice@mail.com "` are the same
person, but they aren't equal strings until you clean up the case and spaces.

## Dates

```python
pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
pd.to_datetime(s, dayfirst=True)        # 03/04 = April 3
s.dt.year, s.dt.month, s.dt.day_name()
```

Passing an explicit `format` is faster and avoids ambiguity (is 03/04 March or April?).

## Derived columns: `assign` and pipelines with `pipe`

```python
clean = (
    raw
    .assign(
        email=lambda d: d["email"].str.strip().str.lower(),
        name=lambda d: d["name"].str.strip().str.title(),
    )
    .dropna(subset=["email"])
    .drop_duplicates(subset=["email"])
    .pipe(parse_amounts, column="balance")    # your own functions in the chain
    .reset_index(drop=True)
)
```

Chaining methods (*method chaining*) makes the process **readable from top to bottom**, with no
intermediate variables, and each step returns a new DataFrame. It's the idiomatic style of
modern pandas.

## Summary

- Diagnosis: `info`, `isna().sum()`, `duplicated` and `value_counts(dropna=False)`.
- Text with `.str` (strip, lower, title, replace with regex, split).
- `pd.to_numeric`/`to_datetime` with `errors="coerce"`; clean local formats first.
- Nulls: `dropna(subset=...)` / `fillna` with judgment; `Int64` for integers with nulls.
- Normalize before `drop_duplicates(subset=...)`.
- Pipelines with `assign` and `pipe`.

## Exercise

The file `customers.csv` has every problem from this chapter. Write the cleaning functions and
the final pipeline.

```
name,email,age,balance,city
  alice SMITH,ALICE@mail.com,31,"$ 1.234,50",Boston
Bob jones ,bob@mail.com ,27,"$ 100,00",boston
carol davis,carol@mail.com,unknown,,Denver
alice smith,alice@mail.com,31,"$ 1.234,50",Boston
...
```

**Further reading:** [Working with text data](https://pandas.pydata.org/docs/user_guide/text.html),
[Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html).
