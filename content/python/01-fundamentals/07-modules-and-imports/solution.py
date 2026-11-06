import importlib
import sys
from importlib.metadata import PackageNotFoundError, version
from types import ModuleType
from typing import Any


def import_object(path: str) -> Any:
    separator = ":" if ":" in path else "."
    module_name, _, attribute = path.rpartition(separator)
    return getattr(importlib.import_module(module_name), attribute)


def public_api(module: ModuleType) -> list[str]:
    names = getattr(module, "__all__", None)
    if names is None:
        names = [n for n in vars(module) if not n.startswith("_")]
    return sorted(names)


def installed_version(package: str) -> str | None:
    try:
        return version(package)
    except PackageNotFoundError:
        return None


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: greet NAME...")
        return 2
    for name in argv:
        print(f"Hello, {name}!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
