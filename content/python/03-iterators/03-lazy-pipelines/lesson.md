# Lazy pipelines

With generators you can build a **pipeline**: a chain of steps (read, parse, filter,
transform, aggregate) where each element goes through every stage before the next one
is read. The result is modular code, easy to test piece by piece, that processes files of
any size with **constant memory**.

## The idea

```python
def read(path):
    with open(path, encoding="utf-8") as f:
        yield from f

def parse(lines):
    for line in lines:
        ip, method, path, status, bytes_ = line.split()
        yield {"ip": ip, "status": int(status), "bytes": int(bytes_)}

def only_errors(records):
    return (r for r in records if r["status"] >= 500)

errors = only_errors(parse(read("access.log")))
for e in errors:
    print(e)
```

Until the `for` loop asks for the first element, **not a single line has been read**. After that, the flow is:

```
for asks → only_errors asks → parse asks → read reads ONE line
         ← filters (or asks again) ← parses        ←
```

At any moment there is **a single record** in memory, not the whole file. A 50 GB file
is processed the same way as a 50 KB one.

## Compared with the "eager" version

```python
lines = open(path).readlines()                   # the whole file in memory
records = [parse_line(l) for l in lines]         # another, bigger copy
errors = [r for r in records if r["status"] >= 500]
```

Each step materializes a full list. It works with small files and blows up with
big ones. It also can't "stop early": if you only want the first 10 errors, it still
processes everything.

## Stopping early: `islice`, `next`, `any`

Since the pipeline is lazy, **asking for less means doing less work**:

```python
from itertools import islice

first_10 = list(islice(errors, 10))                  # reads only what's needed
has_error = any(r["status"] >= 500 for r in recs)    # stops at the first one
first_admin = next((u for u in users if u.admin), None)
```

`islice(it, n)` is "slicing" for iterators, which don't support `it[:10]`.

## Stages as small functions

Each stage takes an iterable and returns an iterable. This has several advantages:

- **They can be tested on their own**: `list(parse(["1.2.3.4 GET / 200 512"]))`, no files needed.
- **They can be combined** in whatever order you need.
- **They can be reused**: `only_errors` works for records coming from a file, an API or
  a database.

A useful convention is for the **last** stage to be the one that materializes or aggregates (`list`, `sum`,
`Counter`, `dict`, writing to a file) and for all the previous ones to be lazy.

## Grouping into batches

The destination often prefers to receive many items at once: database inserts, API calls
with a size limit. The classic pattern uses `islice` and the walrus operator:

```python
from itertools import islice

def in_batches(iterable, n):
    it = iter(iterable)                     # important! a single shared iterator
    while batch := tuple(islice(it, n)):
        yield batch

for batch in in_batches(records, 1000):
    db.insert_many(batch)
```

The `iter()` at the start is key: if `iterable` is a list, each `islice(lst, n)`
would start over from the beginning and the loop would never end.

Since Python 3.12 there's `itertools.batched(iterable, n)`, which does the same thing.

## Handling errors in a stage

Real data always has malformed lines. The usual approach is for the parsing stage to
**skip them and keep count** (or log them), instead of breaking the whole pipeline:

```python
def parse(lines):
    for n, line in enumerate(lines, start=1):
        try:
            ip, _, _, status, bytes_ = line.split()
            yield ip, int(status), int(bytes_)
        except ValueError:
            log.warning("invalid line %d: %r", n, line)
```

## Caveats

- **A pipeline is consumed once.** If you need two results (say, the total and the top
  10), either do both in a single pass or build the pipeline again.
- **The file must stay open** while it's being consumed. If `read()` opens it with `with`
  **inside** the generator, you're fine. If you open it with `with` outside and return the generator
  out of the block, you'll be reading a closed file.
- **Errors show up late**: an exception in `parse` only fires when someone
  consumes, far from where you built the pipeline.

## Summary

- Chain generators: each stage takes an iterable and returns another.
- Constant memory, and the option to stop early with `islice`, `next` or `any`.
- The last stage materializes or aggregates.
- Batches with `iter()` + `islice` + walrus (or `itertools.batched` in 3.12+).
- Skip and record bad data instead of breaking the pipeline.

## Exercise

A pipeline over an infinite source, lazy batches and a small access-log analyzer
built in stages.

**Further reading:** David Beazley, [Generator Tricks for Systems Programmers](https://www.dabeaz.com/generators/)
(a classic, still relevant).
