import re
import tomllib

_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_MINIMUM = re.compile(r">=\s*(\d+)\.(\d+)")


def package_name(specifier: str) -> str:
    m = _NAME.match(specifier.strip())
    if m is None:
        raise ValueError(f"invalid specifier: {specifier!r}")
    return m.group().lower()


def dependencies(pyproject_text: str) -> list[str]:
    data = tomllib.loads(pyproject_text)
    specs = data.get("project", {}).get("dependencies", [])
    return sorted(package_name(s) for s in specs)


def groups(pyproject_text: str) -> dict[str, list[str]]:
    data = tomllib.loads(pyproject_text)
    return {
        group: [package_name(s) for s in specs]
        for group, specs in data.get("dependency-groups", {}).items()
    }


def min_python(pyproject_text: str) -> tuple[int, int] | None:
    requires = tomllib.loads(pyproject_text).get("project", {}).get("requires-python")
    if requires and (m := _MINIMUM.search(requires)):
        return int(m[1]), int(m[2])
    return None
