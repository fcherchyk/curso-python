"""Old (Spanish) module and chapter slugs mapped to the current English ones.

The course used Spanish slugs until November 2026. This map lets the app import progress
saved under the old ids (see `Progress.import_legacy`) and redirect old URLs.
"""

from __future__ import annotations

MODULES: dict[str, str] = {
    "01-fundamentos": "01-fundamentals",
    "02-idiomatico": "02-idiomatic",
    "03-iteradores": "03-iterators",
    "04-funciones": "04-functions",
    "05-modelado": "05-modeling",
    "06-moderno": "06-modern",
    "07-herramientas": "07-tooling",
    "08-flask": "08-flask",
    "09-fastapi": "09-fastapi",
    "10-django": "10-django",
    "11-numpy": "11-numpy",
    "12-pandas": "12-pandas",
    "13-matplotlib": "13-matplotlib",
    "14-finanzas": "14-finance",
}

# Keyed by the OLD module slug, then the old chapter slug.
CHAPTERS: dict[str, dict[str, str]] = {
    "01-fundamentos": {
        "01-objetos-y-mutabilidad": "01-objects-and-mutability",
        "02-listas-tuplas-slicing": "02-lists-tuples-slicing",
        "03-dicts-y-sets": "03-dicts-and-sets",
        "04-control-de-flujo": "04-control-flow",
        "05-funciones-y-firmas": "05-functions-and-signatures",
        "06-excepciones": "06-exceptions",
        "07-modulos-e-imports": "07-modules-and-imports",
    },
    "02-idiomatico": {
        "01-comprehensions": "01-comprehensions",
        "02-desempaquetado": "02-unpacking",
        "03-iterar-bien": "03-iterating-well",
        "04-ordenar": "04-sorting",
        "05-dicts-y-collections": "05-dicts-and-collections",
        "06-strings": "06-strings",
    },
    "03-iteradores": {
        "01-protocolo-de-iteracion": "01-iteration-protocol",
        "02-generadores": "02-generators",
        "03-pipelines-perezosos": "03-lazy-pipelines",
        "04-itertools": "04-itertools",
    },
    "04-funciones": {
        "01-funciones-como-objetos": "01-functions-as-objects",
        "02-closures": "02-closures",
        "03-decoradores": "03-decorators",
        "04-decoradores-con-parametros": "04-decorators-with-parameters",
        "05-context-managers": "05-context-managers",
    },
    "05-modelado": {
        "01-clases-y-dunder": "01-classes-and-dunders",
        "02-property-y-classmethod": "02-property-and-classmethod",
        "03-dataclasses": "03-dataclasses",
        "04-enums": "04-enums",
        "05-protocol-vs-abc": "05-protocol-vs-abc",
        "06-typing-y-genericos": "06-typing-and-generics",
    },
    "06-moderno": {
        "01-match-case": "01-match-case",
        "02-walrus": "02-walrus",
        "03-exception-groups": "03-exception-groups",
        "04-novedades-3-9-a-3-14": "04-whats-new-3-9-to-3-14",
    },
    "07-herramientas": {
        "01-uv-y-pyproject": "01-uv-and-pyproject",
        "02-ruff-y-mypy": "02-ruff-and-mypy",
        "03-pytest-basico": "03-pytest-basics",
        "04-pytest-fixtures-y-mocks": "04-pytest-fixtures-and-mocks",
        "05-proyecto-cli": "05-cli-project",
    },
    "08-flask": {
        "01-primera-app": "01-first-app",
        "02-plantillas-jinja": "02-jinja-templates",
        "03-formularios-y-sesiones": "03-forms-and-sessions",
        "04-app-factory-y-blueprints": "04-app-factory-and-blueprints",
        "05-flask-sqlalchemy": "05-flask-sqlalchemy",
        "06-api-errores-y-auth": "06-api-errors-and-auth",
    },
    "09-fastapi": {
        "01-primera-api": "01-first-api",
        "02-pydantic": "02-pydantic",
        "03-dependencias": "03-dependencies",
        "04-async": "04-async",
        "05-sqlalchemy": "05-sqlalchemy",
        "06-estructura-errores-middleware": "06-structure-errors-middleware",
    },
    "10-django": {
        "01-urls-y-vistas": "01-urls-and-views",
        "02-modelos-y-orm": "02-models-and-orm",
        "03-plantillas-y-formularios": "03-templates-and-forms",
        "04-vistas-genericas-y-admin": "04-generic-views-and-admin",
        "05-django-rest-framework": "05-django-rest-framework",
        "06-autenticacion-y-permisos": "06-authentication-and-permissions",
    },
    "11-numpy": {
        "01-arrays-y-dtypes": "01-arrays-and-dtypes",
        "02-vectorizacion": "02-vectorization",
        "03-mascaras-y-broadcasting": "03-masks-and-broadcasting",
        "04-agregaciones-y-aleatoriedad": "04-aggregations-and-randomness",
    },
    "12-pandas": {
        "01-series-y-dataframe": "01-series-and-dataframe",
        "02-seleccion": "02-selection",
        "03-limpieza": "03-cleaning",
        "04-groupby": "04-groupby",
        "05-merge-y-concat": "05-merge-and-concat",
        "06-series-de-tiempo": "06-time-series",
    },
    "13-matplotlib": {
        "01-figure-y-axes": "01-figure-and-axes",
        "02-tipos-de-grafico": "02-chart-types",
        "03-subplots-y-anotaciones": "03-subplots-and-annotations",
        "04-graficar-desde-pandas": "04-plotting-from-pandas",
    },
    "14-finanzas": {
        "01-precios-y-retornos": "01-prices-and-returns",
        "02-riesgo": "02-risk",
        "03-metricas-ajustadas-por-riesgo": "03-risk-adjusted-metrics",
        "04-portafolios": "04-portfolios",
        "05-frontera-eficiente": "05-efficient-frontier",
        "06-backtesting": "06-backtesting",
    },
}

# Before multi-course support, ids had no course prefix; Python was the only course.
DEFAULT_COURSE = "python"


def translate_path(module: str, chapter: str) -> tuple[str, str] | None:
    """Maps an old `module/chapter` pair to the new one, or None if it is not a legacy id."""
    chapters = CHAPTERS.get(module)
    if chapters is None or chapter not in chapters:
        return None
    return MODULES[module], chapters[chapter]


def translate_id(old_id: str) -> str:
    """Maps a legacy progress id (`module/chapter` or `course/module/chapter`) to the new id.

    Ids that are not legacy are returned unchanged.
    """
    parts = old_id.split("/")
    if len(parts) == 2:
        parts = [DEFAULT_COURSE, *parts]
    if len(parts) != 3:
        return old_id
    course, module, chapter = parts
    new = translate_path(module, chapter)
    return f"{course}/{new[0]}/{new[1]}" if new else "/".join(parts)
