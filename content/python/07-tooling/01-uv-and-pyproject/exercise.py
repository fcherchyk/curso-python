"""uv and pyproject.toml: reading a project's configuration."""

import re  # noqa: F401
import tomllib  # noqa: F401


def package_name(specifier: str) -> str:
    """Package name from a dependency specifier, without extras or versions,
    in lowercase.

    >>> package_name("httpx[http2]>=0.27")
    'httpx'
    >>> package_name("Pydantic >=2,<3")
    'pydantic'

    Hint: the name is letters, digits, `-`, `_` and `.` from the start.
    """
    raise NotImplementedError("TODO")


def dependencies(pyproject_text: str) -> list[str]:
    """Names of the runtime dependencies (`[project] dependencies`), sorted.
    Without the section, an empty list.
    """
    raise NotImplementedError("TODO")


def groups(pyproject_text: str) -> dict[str, list[str]]:
    """Each group in `[dependency-groups]` with the names of its packages (in the order
    they appear).
    """
    raise NotImplementedError("TODO")


def min_python(pyproject_text: str) -> tuple[int, int] | None:
    """Minimum Python version from `requires-python` (only the ">=X.Y" form is used),
    as a tuple. None if it isn't declared.

    >>> min_python('[project]\\nrequires-python = ">=3.12"')
    (3, 12)
    """
    raise NotImplementedError("TODO")
