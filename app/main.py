"""App web del curso: lectura → cuestionario → ejercicio con tests.

uv run uvicorn app.main:app --reload
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Literal

from fastapi import FastAPI, Form, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import render
from app.contenido import RAIZ_CONTENIDO, Capitulo, Curso, cargar_cursos
from app.progreso import Estado, Progreso
from app.quiz import UMBRAL_APROBACION, corregir

AQUI = Path(__file__).resolve().parent
DB_POR_DEFECTO = AQUI.parent / "progreso.db"
COOKIE_CURSO = "curso"


def crear_app(
    raiz_contenido: Path = RAIZ_CONTENIDO,
    ruta_db: Path | None = None,
    recargar_contenido: bool = True,
) -> FastAPI:
    app = FastAPI(title="Cursos de programación", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=AQUI / "static"), name="static")

    plantillas = Jinja2Templates(directory=AQUI / "templates")
    plantillas.env.filters["markdown"] = render.markdown
    plantillas.env.filters["markdown_inline"] = render.markdown_inline
    plantillas.env.globals["UMBRAL"] = int(UMBRAL_APROBACION * 100)
    # Cache-busting de app.css/app.js: cambia cuando se edita cualquier estático.
    plantillas.env.globals["V"] = max(int(p.stat().st_mtime) for p in (AQUI / "static").iterdir())

    progreso = Progreso(ruta_db or Path(os.environ.get("CURSO_DB", DB_POR_DEFECTO)))
    progreso.migrar_ids_sin_curso("python")
    cache: dict[str, list[Curso]] = {}

    def cursos() -> list[Curso]:
        # En desarrollo se relee el contenido en cada request para ver cambios al instante.
        if recargar_contenido or "c" not in cache:
            cache["c"] = cargar_cursos(raiz_contenido)
        return cache["c"]

    def buscar_curso(slug: str) -> Curso:
        curso = next((c for c in cursos() if c.slug == slug), None)
        if curso is None:
            raise HTTPException(404, "Curso no encontrado")
        return curso

    def buscar(curso: str, modulo: str, cap: str) -> tuple[Curso, Capitulo]:
        c = buscar_curso(curso)
        capitulo = c.capitulo(modulo, cap)
        if capitulo is None:
            raise HTTPException(404, "Capítulo no encontrado")
        return c, capitulo

    def pagina(
        request: Request, plantilla: str, curso: Curso, contexto: dict[str, object]
    ) -> HTMLResponse:
        respuesta = plantillas.TemplateResponse(
            request, plantilla, {"cursos": cursos(), "curso": curso, **contexto}
        )
        respuesta.set_cookie(COOKIE_CURSO, curso.slug, max_age=60 * 60 * 24 * 365)
        return respuesta

    @app.get("/pygments.css", include_in_schema=False)
    def pygments_css() -> Response:
        return Response(render.css_pygments(), media_type="text/css")

    @app.get("/", include_in_schema=False)
    def raiz(request: Request) -> RedirectResponse:
        slugs = [c.slug for c in cursos()]
        preferido = request.cookies.get(COOKIE_CURSO)
        return RedirectResponse(f"/{preferido if preferido in slugs else slugs[0]}")

    @app.get("/c/{modulo}/{cap}", include_in_schema=False)
    def url_vieja(modulo: str, cap: str) -> RedirectResponse:
        # Antes de los cursos, los capítulos de Python vivían en /c/{modulo}/{cap}.
        return RedirectResponse(f"/c/python/{modulo}/{cap}", status_code=301)

    @app.get("/{curso}", response_class=HTMLResponse)
    def indice(request: Request, curso: str) -> HTMLResponse:
        c = buscar_curso(curso)
        estados = progreso.todos()
        siguiente = next(
            (cap for cap in c.capitulos() if not estados.get(cap.id, Estado()).completo), None
        )
        completos = {
            m.slug: sum(estados.get(cap.id, Estado()).completo for cap in m.capitulos)
            for m in c.modulos
        }
        return pagina(
            request,
            "index.html",
            c,
            {"estados": estados, "siguiente": siguiente, "completos": completos},
        )

    @app.get("/c/{curso}/{modulo}/{cap}", response_class=HTMLResponse)
    def capitulo(request: Request, curso: str, modulo: str, cap: str) -> HTMLResponse:
        cur, c = buscar(curso, modulo, cap)
        estado = progreso.estado(c.id)
        anterior, siguiente = cur.vecinos(c)
        return pagina(
            request,
            "capitulo.html",
            cur,
            {
                "cap": c,
                "modulo": cur.modulo(c.modulo),
                "estados": progreso.todos(),
                "estado": estado,
                "leccion": render.markdown(c.leccion()),
                "preguntas": c.preguntas(),
                "codigo": estado.codigo if estado.codigo is not None else c.codigo_inicial(),
                "anterior": anterior,
                "siguiente": siguiente,
            },
        )

    @app.post("/c/{curso}/{modulo}/{cap}/leido", response_class=HTMLResponse)
    def marcar_leido(request: Request, curso: str, modulo: str, cap: str) -> HTMLResponse:
        _, c = buscar(curso, modulo, cap)
        progreso.marcar_leido(c.id, not progreso.estado(c.id).leido)
        return plantillas.TemplateResponse(
            request, "_leido.html", {"cap": c, "estado": progreso.estado(c.id)}
        )

    @app.post("/c/{curso}/{modulo}/{cap}/{paso}/resuelto", response_class=HTMLResponse)
    def marcar_resuelto(
        request: Request, curso: str, modulo: str, cap: str, paso: Literal["quiz", "tests"]
    ) -> HTMLResponse:
        """Alterna a mano un paso, para saltearlo sin hacerlo. Cuenta igual que aprobarlo."""
        _, c = buscar(curso, modulo, cap)
        actual = progreso.estado(c.id)
        if paso == "quiz":
            progreso.marcar_quiz(c.id, not actual.quiz_ok)
        else:
            progreso.marcar_tests(c.id, not actual.tests_ok)
        estado = progreso.estado(c.id)
        ok = estado.quiz_ok if paso == "quiz" else estado.tests_ok
        return plantillas.TemplateResponse(
            request, "_resuelto.html", {"cap": c, "paso": paso, "ok": ok, "estado": estado}
        )

    @app.post("/c/{curso}/{modulo}/{cap}/quiz", response_class=HTMLResponse)
    async def responder_quiz(request: Request, curso: str, modulo: str, cap: str) -> HTMLResponse:
        _, c = buscar(curso, modulo, cap)
        preguntas = c.preguntas()
        form = await request.form()
        elegidas: dict[int, int | None] = {}
        for i in range(len(preguntas)):
            valor = form.get(f"p{i}")
            elegidas[i] = int(valor) if isinstance(valor, str) and valor.isdigit() else None
        resultado = corregir(preguntas, elegidas)
        progreso.registrar_quiz(c.id, resultado.puntaje, resultado.aprobado)
        return plantillas.TemplateResponse(
            request,
            "_quiz.html",
            {
                "cap": c,
                "preguntas": preguntas,
                "resultado": resultado,
                "estado": progreso.estado(c.id),
            },
        )

    @app.post("/c/{curso}/{modulo}/{cap}/codigo", status_code=204)
    def guardar_codigo(
        curso: str, modulo: str, cap: str, codigo: Annotated[str, Form()]
    ) -> Response:
        _, c = buscar(curso, modulo, cap)
        progreso.guardar_codigo(c.id, codigo)
        return Response(status_code=204)

    @app.post("/c/{curso}/{modulo}/{cap}/tests", response_class=HTMLResponse)
    async def ejecutar_tests(
        request: Request, curso: str, modulo: str, cap: str, codigo: Annotated[str, Form()]
    ) -> HTMLResponse:
        _, c = buscar(curso, modulo, cap)
        resultado = await run_in_threadpool(c.lenguaje.correr, codigo, c.archivos_de_soporte())
        progreso.registrar_tests(c.id, codigo, resultado.aprobado)
        return plantillas.TemplateResponse(
            request,
            "_tests_resultado.html",
            {"cap": c, "resultado": resultado, "estado": progreso.estado(c.id)},
        )

    @app.get("/c/{curso}/{modulo}/{cap}/solucion", response_class=HTMLResponse)
    def ver_solucion(curso: str, modulo: str, cap: str) -> HTMLResponse:
        _, c = buscar(curso, modulo, cap)
        if not progreso.estado(c.id).tests_ok:
            return HTMLResponse(
                '<p class="aviso">La solución se habilita cuando pasan todos los tests.</p>'
            )
        return HTMLResponse(str(render.codigo_html(c.solucion(), c.lenguaje.lexer)))

    @app.get("/c/{curso}/{modulo}/{cap}/inicial", response_class=PlainTextResponse)
    def codigo_inicial(curso: str, modulo: str, cap: str) -> str:
        return buscar(curso, modulo, cap)[1].codigo_inicial()

    return app


app = crear_app()
