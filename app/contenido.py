"""Carga de los cursos desde `contenido/`.

Estructura esperada:

    contenido/
      <curso>/
        curso.toml               # titulo, lenguaje (python | go), orden, descripcion
        NN-modulo/
          modulo.toml            # titulo, descripcion
          NN-capitulo/
            leccion.md           # la primera línea `# Título` es el título del capítulo
            quiz.toml            # [[preguntas]] texto, opciones, correcta (0-based), explicacion
            <ejercicio>          # código inicial      (ejercicio.py | ejercicio.go)
            <tests>              # tests               (test_ejercicio.py | ejercicio_test.go)
            <solucion>           # solución de referencia (solucion.py | solucion.go)
            ...                  # archivos de soporte que necesitan los tests
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from app.lenguajes import LENGUAJES, Lenguaje

RAIZ_CONTENIDO = Path(__file__).resolve().parent.parent / "contenido"


@dataclass(frozen=True)
class Pregunta:
    texto: str
    opciones: list[str]
    correcta: int
    explicacion: str = ""


@dataclass
class Capitulo:
    curso: str
    modulo: str
    slug: str
    titulo: str
    ruta: Path
    lenguaje: Lenguaje

    @property
    def id(self) -> str:
        return f"{self.curso}/{self.modulo}/{self.slug}"

    @property
    def numero(self) -> str:
        return self.slug.split("-", 1)[0]

    def leccion(self) -> str:
        """Markdown de la lección sin la línea de título."""
        texto = (self.ruta / "leccion.md").read_text(encoding="utf-8")
        primera, _, resto = texto.partition("\n")
        return resto if primera.startswith("# ") else texto

    def preguntas(self) -> list[Pregunta]:
        ruta = self.ruta / "quiz.toml"
        if not ruta.exists():
            return []
        datos = tomllib.loads(ruta.read_text(encoding="utf-8"))
        return [Pregunta(**p) for p in datos.get("preguntas", [])]

    def codigo_inicial(self) -> str:
        return (self.ruta / self.lenguaje.archivo_ejercicio).read_text(encoding="utf-8")

    def solucion(self) -> str:
        return (self.ruta / self.lenguaje.archivo_solucion).read_text(encoding="utf-8")

    @property
    def archivo_tests(self) -> Path:
        return self.ruta / self.lenguaje.archivo_tests

    def archivos_de_soporte(self) -> list[Path]:
        """Tests, datos y carpetas (p. ej. `templates/`) que necesita el ejercicio."""
        privados = self.lenguaje.archivos_privados
        return [
            p
            for p in sorted(self.ruta.iterdir())
            if p.name not in privados
            and not p.name.startswith((".", "__pycache__"))
            and (p.is_file() or p.is_dir())
        ]


@dataclass
class Modulo:
    slug: str
    titulo: str
    descripcion: str
    capitulos: list[Capitulo] = field(default_factory=list)

    @property
    def numero(self) -> str:
        return self.slug.split("-", 1)[0]


@dataclass
class Curso:
    slug: str
    titulo: str
    descripcion: str
    lenguaje: Lenguaje
    orden: int
    modulos: list[Modulo] = field(default_factory=list)

    def capitulos(self) -> list[Capitulo]:
        return [c for m in self.modulos for c in m.capitulos]

    def capitulo(self, modulo: str, slug: str) -> Capitulo | None:
        return next((c for c in self.capitulos() if c.modulo == modulo and c.slug == slug), None)

    def modulo(self, slug: str) -> Modulo | None:
        return next((m for m in self.modulos if m.slug == slug), None)

    def vecinos(self, cap: Capitulo) -> tuple[Capitulo | None, Capitulo | None]:
        todos = self.capitulos()
        i = next(i for i, c in enumerate(todos) if c.id == cap.id)
        anterior = todos[i - 1] if i > 0 else None
        siguiente = todos[i + 1] if i + 1 < len(todos) else None
        return anterior, siguiente


def _titulo_de(leccion: Path, por_defecto: str) -> str:
    with leccion.open(encoding="utf-8") as f:
        primera = f.readline().strip()
    return primera.removeprefix("# ").strip() if primera.startswith("# ") else por_defecto


def _leer_toml(ruta: Path) -> dict[str, object]:
    return tomllib.loads(ruta.read_text(encoding="utf-8"))


def cargar_curso(dir_curso: Path) -> Curso:
    meta = _leer_toml(dir_curso / "curso.toml")
    lenguaje = LENGUAJES[str(meta["lenguaje"])]
    curso = Curso(
        slug=dir_curso.name,
        titulo=str(meta.get("titulo", dir_curso.name)),
        descripcion=str(meta.get("descripcion", "")),
        lenguaje=lenguaje,
        orden=int(meta.get("orden", 99)),  # type: ignore[call-overload]
    )
    for dir_mod in sorted(p for p in dir_curso.iterdir() if (p / "modulo.toml").exists()):
        meta_mod = _leer_toml(dir_mod / "modulo.toml")
        modulo = Modulo(
            slug=dir_mod.name,
            titulo=str(meta_mod.get("titulo", dir_mod.name)),
            descripcion=str(meta_mod.get("descripcion", "")),
        )
        for dir_cap in sorted(p for p in dir_mod.iterdir() if (p / "leccion.md").exists()):
            modulo.capitulos.append(
                Capitulo(
                    curso=curso.slug,
                    modulo=dir_mod.name,
                    slug=dir_cap.name,
                    titulo=_titulo_de(dir_cap / "leccion.md", dir_cap.name),
                    ruta=dir_cap,
                    lenguaje=lenguaje,
                )
            )
        curso.modulos.append(modulo)
    return curso


def cargar_cursos(raiz: Path = RAIZ_CONTENIDO) -> list[Curso]:
    cursos = [cargar_curso(d) for d in raiz.iterdir() if (d / "curso.toml").exists()]
    return sorted(cursos, key=lambda c: (c.orden, c.slug))
