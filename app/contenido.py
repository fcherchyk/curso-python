"""Carga del temario desde `contenido/`.

Estructura esperada:

    contenido/
      NN-modulo/
        modulo.toml            # titulo, descripcion
        NN-capitulo/
          leccion.md           # la primera línea `# Título` es el título del capítulo
          quiz.toml            # [[preguntas]] texto, opciones, correcta (0-based), explicacion
          ejercicio.py         # código inicial
          test_ejercicio.py    # tests (importan `from ejercicio import ...`)
          solucion.py          # solución de referencia
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

RAIZ_CONTENIDO = Path(__file__).resolve().parent.parent / "contenido"

# Archivos de un capítulo que NO se copian al directorio donde corren los tests.
ARCHIVOS_PRIVADOS = {"leccion.md", "quiz.toml", "solucion.py", "ejercicio.py"}


@dataclass(frozen=True)
class Pregunta:
    texto: str
    opciones: list[str]
    correcta: int
    explicacion: str = ""


@dataclass
class Capitulo:
    modulo: str
    slug: str
    titulo: str
    ruta: Path

    @property
    def id(self) -> str:
        return f"{self.modulo}/{self.slug}"

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
        return (self.ruta / "ejercicio.py").read_text(encoding="utf-8")

    def solucion(self) -> str:
        return (self.ruta / "solucion.py").read_text(encoding="utf-8")

    @property
    def archivo_tests(self) -> Path:
        return self.ruta / "test_ejercicio.py"

    def archivos_de_soporte(self) -> list[Path]:
        """Tests y archivos de datos que necesita el ejercicio para correr."""
        return [
            p
            for p in sorted(self.ruta.iterdir())
            if p.is_file() and p.name not in ARCHIVOS_PRIVADOS and not p.name.startswith(".")
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
class Temario:
    modulos: list[Modulo]

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


def cargar_temario(raiz: Path = RAIZ_CONTENIDO) -> Temario:
    modulos: list[Modulo] = []
    for dir_mod in sorted(p for p in raiz.iterdir() if (p / "modulo.toml").exists()):
        meta = tomllib.loads((dir_mod / "modulo.toml").read_text(encoding="utf-8"))
        modulo = Modulo(
            slug=dir_mod.name,
            titulo=meta.get("titulo", dir_mod.name),
            descripcion=meta.get("descripcion", ""),
        )
        for dir_cap in sorted(p for p in dir_mod.iterdir() if (p / "leccion.md").exists()):
            modulo.capitulos.append(
                Capitulo(
                    modulo=dir_mod.name,
                    slug=dir_cap.name,
                    titulo=_titulo_de(dir_cap / "leccion.md", dir_cap.name),
                    ruta=dir_cap,
                )
            )
        modulos.append(modulo)
    return Temario(modulos)
