# Modules, Packages and Imports

Every `.py` file is a **module**, and a folder of modules is a **package**. Understanding how
Python finds and runs what you import saves you from the most frustrating everyday errors,
like `ModuleNotFoundError`, circular imports or code that runs "by itself" on import.

## What happens when you do `import x`

1. Python looks for `x` in `sys.modules`, the cache of already-imported modules. If it's
   there, it reuses it.
2. If not, it searches the directories in `sys.path`: first the directory of the script you
   ran (or the current one), then `PYTHONPATH` and finally the stdlib and `site-packages`.
3. It finds it and **runs the whole file, top to bottom**, exactly once.
4. It stores the module object in `sys.modules` and binds it to the name `x`.

Step 3 is key: **importing runs code**. That's why a module shouldn't do heavy work or have
side effects (connecting to a database, printing, reading files) at the top level.

## Ways to import

```python
import json                        # you use json.loads(...)
import numpy as np                 # alias (community convention)
from pathlib import Path           # bring in a specific name
from os import path as osp
from collections import Counter, defaultdict
```

- `import module` makes it clear where each thing comes from (`json.loads`).
- `from module import name` is convenient for frequently used, unambiguous names (`Path`).
- **Avoid `from module import *`**: it pollutes the namespace, hides where names come from
  and confuses tools.

Conventional order (ruff sorts it for you with the `I` rule): stdlib, then third-party and
finally your project, in blocks separated by a blank line.

## `if __name__ == "__main__":`

Every module has a `__name__` variable. It's the module's name when it's **imported**
(`"utils"`) and `"__main__"` when it's **run** directly (`python utils.py`):

```python
# utils.py
def main(argv: list[str]) -> int:
    print("processing", argv)
    return 0

if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
```

That way the file works both as a library (it imports without side effects) and as a script.
Having a `main(argv) -> int` function instead of loose code also makes it **testable**.

`python -m package.module` runs a module as a script using the package's import resolution.
It's the recommended way to run modules that live inside packages, and also to run tools:
`python -m pytest`, `python -m http.server`.

## Packages

```
shop/
├── __init__.py          # runs when "shop" is imported
├── models.py
└── payments/
    ├── __init__.py
    └── card.py
```

```python
from shop.models import Product
from shop.payments import card
```

`__init__.py` can be empty. It's often used to expose the package's public API:

```python
# shop/__init__.py
from shop.models import Product, Order

__all__ = ["Product", "Order"]
```

`__all__` defines what `import *` exports and documents the public API. By convention, names
starting with `_` are **private**: nothing enforces it, but they say "don't rely on this".

### Absolute vs. relative imports

```python
# inside shop/payments/card.py
from shop.models import Order          # absolute: recommended
from ..models import Order             # relative: only valid inside a package
```

Relative imports don't work if you run the file directly (`python card.py`), and that's a
classic source of `ImportError: attempted relative import with no known parent package`. The
fix is to run it as `python -m shop.payments.card`.

## Circular imports

If `a.py` imports `b` and `b.py` imports `a`, one of them will find the other **half-executed**,
with names that don't exist yet. Fixes, in order of preference:

1. **Restructure**: move the shared code to a third module.
2. Import the whole module (`import a`) instead of names (`from a import X`) and use `a.X`
   inside functions.
3. Import inside the function that needs it (last resort).
4. If the import is only for type annotations: `if TYPE_CHECKING:`.

## Dynamic imports

Sometimes the module name is only known at runtime (plugins, configuration):

```python
import importlib

module = importlib.import_module("json")
function = getattr(module, "dumps")
```

That's how strings like `"app.main:app"` that you pass to uvicorn work.

To query metadata of installed packages:

```python
from importlib.metadata import version, PackageNotFoundError
version("pytest")        # '8.4.1'
```

## Modules, environments and `uv`

Third-party packages are installed into the `site-packages` **of the active virtual
environment**. With `uv`, each project has its own `.venv`; `uv add package` installs it and
records it in `pyproject.toml`, and `uv run command` runs with that environment. We cover it
in detail in the tooling module.

## Summary

- Importing runs the module once and caches it in `sys.modules`.
- Don't put side effects at the top level; use `if __name__ == "__main__":` and a
  `main(argv) -> int` function.
- No `import *`. Absolute over relative. `__all__` and `_private` for the API.
- Circular imports: restructure.
- `importlib.import_module` + `getattr` for dynamic imports.

## Exercise

Four functions: a dynamic import by path, listing a module's public API, checking installed
versions and a testable `main` with its guard.

**Further reading:** [The import system](https://docs.python.org/3/reference/import.html),
[Modules (tutorial)](https://docs.python.org/3/tutorial/modules.html).
