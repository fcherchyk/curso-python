# ExceptionGroup, `except*` and notes

Up to 3.10, an exception represented **one** error. But there are situations where **several
happen at once** and you want to report them all together: validating a whole form, running
tasks in parallel where two of them fail, or processing a batch with errors in different rows.
For that, 3.11 added `ExceptionGroup`, the `except*` syntax and notes on exceptions.

## `ExceptionGroup`: several exceptions in one

```python
errors = [ValueError("empty name"), TypeError("age is not an int")]
raise ExceptionGroup("invalid user", errors)
```

The traceback shows a tree with every error:

```
  | ExceptionGroup: invalid user (2 sub-exceptions)
  +-+---------------- 1 ----------------
    | ValueError: empty name
    +---------------- 2 ----------------
    | TypeError: age is not an int
    +------------------------------------
```

- The first argument is a message; the second, a **non-empty sequence** of exceptions.
- `.exceptions` gives you the tuple of sub-exceptions.
- Groups can be **nested**: a group can contain other groups.
- If every sub-exception inherits from `Exception`, you get an `ExceptionGroup`; if any is a
  `BaseException` (like `KeyboardInterrupt`), a `BaseExceptionGroup`.

### The pattern: collect and raise at the end

```python
def validate(data: dict) -> None:
    errors: list[Exception] = []
    if not data.get("name"):
        errors.append(ValueError("name"))
    if not isinstance(data.get("age"), int):
        errors.append(TypeError("age"))
    if errors:
        raise ExceptionGroup("invalid data", errors)
```

Someone filling out a form is much better served by getting **all** the problems at once than
by fixing them one per attempt.

## `except*`: handling by type inside the group

A regular `except ValueError` does **not** catch an `ExceptionGroup` that contains
`ValueError`s. That's what `except*` is for:

```python
try:
    validate(data)
except* ValueError as group:          # group is an ExceptionGroup with ONLY the ValueErrors
    for e in group.exceptions:
        print("invalid value:", e)
except* TypeError as group:           # this branch ALSO runs if there are TypeErrors!
    for e in group.exceptions:
        print("invalid type:", e)
```

Differences from the classic `except`:

- **Several branches can run**: each one takes "its share" of the group.
- In each branch, the variable is **a group** (filtered), not a single exception.
- Whatever no branch handled is **re-raised** automatically as a group with what's left.
- You can't mix `except` and `except*` in the same `try`.
- `except*` also catches a regular (ungrouped) exception: it wraps it in a group.

### Filtering by hand: `split` and `subgroup`

```python
values, rest = group.split(ValueError)        # (group with ValueErrors, group with the rest)
only_values = group.subgroup(ValueError)      # or None if there are none
```

## Where you'll see them: `asyncio.TaskGroup`

The most common use case is concurrency. If two tasks fail inside a `TaskGroup`, an
`ExceptionGroup` with both is raised (we cover it in the concurrency module):

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(download(url1))
        tg.create_task(download(url2))
except* TimeoutError:
    ...
except* ConnectionError:
    ...
```

## Notes: extra context on any exception

`add_note` (3.11) adds text that shows up in the traceback, **without changing the type or the
message** of the exception. It's ideal for saying *where* the error happened:

```python
for n, row in enumerate(rows, start=1):
    try:
        process(row)
    except ValueError as e:
        e.add_note(f"on row {n}: {row!r}")
        raise
```

```
ValueError: invalid literal for int() with base 10: 'x'
on row 3: 'alice,x'
```

Notes are kept in `e.__notes__` (a list). They're better than wrapping in another exception
when all you want is to add context.

## Summary

- `ExceptionGroup(message, [exceptions])` to report several errors together.
- Collect them in a list and raise the group at the end if it isn't empty.
- `except* Type as group`: several branches can run; whatever isn't handled is re-raised.
- `split` and `subgroup` to filter by hand.
- `e.add_note(...)` to add context without changing the exception.

## Exercise

A validation that reports every error, a classification with `except*` and a task runner that
collects failures with notes.

**Further reading:** [PEP 654 — Exception Groups and except*](https://peps.python.org/pep-0654/),
[PEP 678 — add_note](https://peps.python.org/pep-0678/).
