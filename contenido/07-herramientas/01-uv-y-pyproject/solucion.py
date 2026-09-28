import re
import tomllib

_NOMBRE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_MINIMO = re.compile(r">=\s*(\d+)\.(\d+)")


def nombre_de_paquete(especificador: str) -> str:
    m = _NOMBRE.match(especificador.strip())
    if m is None:
        raise ValueError(f"especificador inválido: {especificador!r}")
    return m.group().lower()


def dependencias(texto_pyproject: str) -> list[str]:
    datos = tomllib.loads(texto_pyproject)
    specs = datos.get("project", {}).get("dependencies", [])
    return sorted(nombre_de_paquete(s) for s in specs)


def grupos(texto_pyproject: str) -> dict[str, list[str]]:
    datos = tomllib.loads(texto_pyproject)
    return {
        grupo: [nombre_de_paquete(s) for s in specs]
        for grupo, specs in datos.get("dependency-groups", {}).items()
    }


def python_minimo(texto_pyproject: str) -> tuple[int, int] | None:
    requiere = tomllib.loads(texto_pyproject).get("project", {}).get("requires-python")
    if requiere and (m := _MINIMO.search(requiere)):
        return int(m[1]), int(m[2])
    return None
