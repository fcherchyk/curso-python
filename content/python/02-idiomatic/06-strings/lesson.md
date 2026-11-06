# Idiomatic strings

Python's `str` is **immutable**, Unicode-based and comes with lots of methods. Most string
bugs come from building them badly (concatenating in loops), parsing them by hand with
indices or not knowing the method that already solves the problem.

## f-strings: the default format

Since 3.6, f-strings are the recommended way to interpolate. They're more readable and
faster than `%` and `.format()`:

```python
name, age = "Alice", 31
f"{name} is {age} years old"
f"{name!r}"              # repr: "'Alice'"  (useful in logs and error messages)
f"{age + 1}"             # any expression
f"{x=}"                  # debug (3.8+): "x=42"
f"{x = }"                # with spaces: "x = 42"
```

### The format mini-language

After the `:` comes a format specification:

```python
price = 1234.5
f"{price:.2f}"           # '1234.50'     2 decimal places
f"{price:,.2f}"          # '1,234.50'    thousands separator
f"{price:_.0f}"          # '1_234'
f"{0.256:.1%}"           # '25.6%'
f"{42:>6}"               # '    42'      right-aligned in 6
f"{'hello':<8}|"         # 'hello   |'   left
f"{'hello':^10}"         # '  hello   '  centered
f"{7:03d}"               # '007'         zero-padded
f"{255:x} {255:b}"       # 'ff 11111111' hex and binary
f"{date:%Y-%m-%d}"       # objects define their own format (datetime)
```

The specification can also come from a variable: `f"{value:>{width}}"`.

> The `,` thousands separator uses the US/English format (`1,234.50`). For the format used
> in Argentina and much of Europe (`1.234,50`) there are two options: `locale` (which depends
> on the system configuration) or swapping the characters after formatting. You'll practice
> this in the exercise.

## Joining and splitting

```python
", ".join(["a", "b", "c"])         # 'a, b, c'  <- join is a method of the SEPARATOR
" ".join(str(n) for n in nums)     # join only accepts strings: convert first

"a,b,,c".split(",")                # ['a', 'b', '', 'c']
"  hello   world ".split()         # ['hello', 'world']  <- no argument: any whitespace, no empties
"k=v=w".split("=", 1)              # ['k', 'v=w']        <- at most 1 split
"path/to/file.txt".rsplit("/", 1)  # ['path/to', 'file.txt']
```

### Never concatenate in a loop

```python
# ✗ Quadratic: each += may copy the whole string
s = ""
for word in words:
    s += word + " "

# ✓ Linear
s = " ".join(words)
```

### `partition`: splitting in three with no surprises

```python
"key=value".partition("=")         # ('key', '=', 'value')
"no-equals".partition("=")         # ('no-equals', '', '')  <- doesn't fail
user, _, domain = email.partition("@")
```

With `split("=")` you have to check how many pieces you got. `partition` always returns a
three-element tuple, so unpacking it never fails.

## Cleaning and querying

```python
"  hello \n".strip()               # 'hello'  (also lstrip / rstrip)
"xxhello".lstrip("x")              # 'hello'  CAREFUL! it removes CHARACTERS, not a prefix
"https://site".removeprefix("https://")    # 'site'  (3.9+) removes the exact prefix
"photo.jpg".removesuffix(".jpg")   # 'photo'

"file.py".endswith((".py", ".pyi"))        # accepts a tuple of options
"ab" in "cabin"                    # substring search
"hello".find("z")                  # -1 (index() would raise ValueError)
"Straße".casefold() == "strasse"   # True: case-insensitive comparison, sturdier than lower()
"42".isdigit(), "abc".isalpha(), "   ".isspace()
```

The `strip("https://")` trap is a classic: it removes any combination of the characters
`h t p s : /` from both ends, not the prefix. For prefixes and suffixes use
`removeprefix` and `removesuffix`.

## Replacing and translating

```python
"a-b-c".replace("-", "_")          # 'a_b_c'
"a-b-c".replace("-", "_", 1)       # 'a_b-c'   only the first one

# translate: several single-character replacements in one pass
table = str.maketrans({",": ".", ".": ","})
"1,234.50".translate(table)        # '1.234,50'
```

`translate` is the right way to **swap** characters. With two `replace` calls in a row, the
second would undo what the first did.

## Multiline and raw strings

```python
sql = """
    SELECT *
    FROM users
"""
import textwrap
textwrap.dedent(sql).strip()       # removes the common indentation

r"C:\new\folder"                   # raw string: \ doesn't escape (useful in regexes and Windows paths)
```

## `str` vs. `bytes`

`str` is Unicode text; `bytes` are octets. You convert at the edges of the program:

```python
"café".encode("utf-8")             # b'caf\xc3\xa9'
b"\xc3\xa9".decode("utf-8")        # 'é'
```

Rule: **decode when reading and encode when writing**. Inside the program always work with
`str`, and open text files with an explicit `encoding="utf-8"`.

## Summary

| You want to…                            | Use                                  |
|-----------------------------------------|--------------------------------------|
| interpolate                             | f-string                             |
| format numbers                          | `f"{x:,.2f}"`, `f"{x:.1%}"`          |
| join many parts                         | `sep.join(parts)`                    |
| split in two on a separator             | `a, _, b = s.partition(sep)`         |
| remove an exact prefix or suffix        | `removeprefix` / `removesuffix`      |
| check several possible endings          | `s.endswith((".a", ".b"))`           |
| swap characters                         | `str.maketrans` + `translate`        |
| compare case-insensitively              | `a.casefold() == b.casefold()`       |

## Exercise

Four functions: format currency the Argentine way, generate a *slug*, parse `key=value`
pairs and build a URL.

**Further reading:** [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec),
[str methods](https://docs.python.org/3/library/stdtypes.html#string-methods).
