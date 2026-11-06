"""Modules, packages and imports."""

import importlib  # noqa: F401
from importlib.metadata import PackageNotFoundError, version  # noqa: F401
from types import ModuleType
from typing import Any


def import_object(path: str) -> Any:
    """Import an object from a string "package.module:name" or
    "package.module.name" (whatever comes after the last `.` or the `:` is the attribute).

    >>> import_object("math:sqrt")(16)
    4.0
    >>> import_object("os.path.join")("a", "b")
    'a/b'
    """
    raise NotImplementedError("TODO")


def public_api(module: ModuleType) -> list[str]:
    """Public names of a module, sorted.

    If the module defines `__all__`, it's those. Otherwise, every name that doesn't start with `_`.
    """
    raise NotImplementedError("TODO")


def installed_version(package: str) -> str | None:
    """Installed version of the package, or None if it isn't installed.

    Hint: `importlib.metadata.version`.
    """
    raise NotImplementedError("TODO")


def main(argv: list[str]) -> int:
    """Entry point: print "Hello, NAME!" for each argument and return 0.
    With no arguments, print "usage: greet NAME..." and return 2.

    Also, add the `__name__` guard (see the lesson) at the end of the file
    that calls `main(sys.argv[1:])` and exits with its result.
    """
    raise NotImplementedError("TODO")
