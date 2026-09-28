"""App web del curso: lectura → cuestionario → ejercicio con tests.

uv run uvicorn app.main:app --reload
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Literal

from fastapi import FastAPI, Form, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import render
from app.contenido import RAIZ_CONTENIDO, Capitulo, Temario, cargar_temario
from app.progreso import Estado, Progreso
from app.quiz import UMBRAL_APROBACION, corregir
from app.runner import correr_tests

AQUI = Path(__file__).resolve().parent
DB_POR_DEFECTO = AQUI.parent / "progreso.db"


def crear_app(
    raiz_contenido: Path = RAIZ_CONTENIDO,
    ruta_db: Path | None = None,
    recargar_contenido: bool = True,
) -> FastAPI:
    app = FastAPI(title="Curso de Python", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=AQUI / "static"), name="static")

    plantillas = Jinja2Templates(directory=AQUI / "templates")
    plantillas.env.filters["markdown"] = render.markdown
    plantillas.env.filters["markdown_inline"] = render.markdown_inline
    plantillas.env.globals["UMBRAL"] = int(UMBRAL_APROBACION * 100)
    # Cache-busting de app.css/app.js: cambia cuando se edita cualquier estático.
    plantillas.env.globals["V"] = max(int(p.stat().st_mtime) for p in (AQUI / "static").iterdir())

    progreso = Progreso(ruta_db or Path(os.environ.get("CURSO_DB", DB_POR_DEFECTO)))
    cache: dict[str, Temario] = {}

    def temario() -> Temario:
        # En desarrollo se relee el contenido en cada request para ver cambios al instante.
        if recargar_contenido or "t" not in cache:
            cache["t"] = cargar_temario(raiz_contenido)
        return cache["t"]

    def buscar(modulo: str, cap: str) -> Capitulo:
        capitulo = temario().capitulo(modulo, cap)
        if capitulo is None:
            raise HTTPException(404, "Capítulo no encontrado")
        return capitulo

    @app.get("/pygments.css", include_in_schema=False)
    def pygments_css() -> Response:
        return Response(render.css_pygments(), media_type="text/css")

    @app.get("/", response_class=HTMLResponse)
    def indice(request: Request) -> HTMLResponse:
        t = temario()
        estados = progreso.todos()
        caps = t.capitulos()
        siguiente = next((c for c in caps if not estados.get(c.id, Estado()).completo), None)
        completos = {
            m.slug: sum(estados.get(c.id, Estado()).completo for c in m.capitulos)
            for m in t.modulos
        }
        return plantillas.TemplateResponse(
            request,
            "index.html",
            {"temario": t, "estados": estados, "siguiente": siguiente, "completos": completos},
        )

    @app.get("/c/{modulo}/{cap}", response_class=HTMLResponse)
    def capitulo(request: Request, modulo: str, cap: str) -> HTMLResponse:
        c = buscar(modulo, cap)
        t = temario()
        estado = progreso.estado(c.id)
        anterior, siguiente = t.vecinos(c)
        return plantillas.TemplateResponse(
            request,
            "capitulo.html",
            {
                "cap": c,
                "modulo": t.modulo(c.modulo),
                "temario": t,
                "estados": progreso.todos(),
                "estado": estado,
                "leccion": render.markdown(c.leccion()),
                "preguntas": c.preguntas(),
                "codigo": estado.codigo if estado.codigo is not None else c.codigo_inicial(),
                "anterior": anterior,
                "siguiente": siguiente,
            },
        )

    @app.post("/c/{modulo}/{cap}/leido", response_class=HTMLResponse)
    def marcar_leido(request: Request, modulo: str, cap: str) -> HTMLResponse:
        c = buscar(modulo, cap)
        progreso.marcar_leido(c.id, not progreso.estado(c.id).leido)
        return plantillas.TemplateResponse(
            request, "_leido.html", {"cap": c, "estado": progreso.estado(c.id)}
        )

    @app.post("/c/{modulo}/{cap}/{paso}/resuelto", response_class=HTMLResponse)
    def marcar_resuelto(
        request: Request, modulo: str, cap: str, paso: Literal["quiz", "tests"]
    ) -> HTMLResponse:
        """Alterna a mano un paso, para saltearlo sin hacerlo. Cuenta igual que aprobarlo."""
        c = buscar(modulo, cap)
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

    @app.post("/c/{modulo}/{cap}/quiz", response_class=HTMLResponse)
    async def responder_quiz(request: Request, modulo: str, cap: str) -> HTMLResponse:
        c = buscar(modulo, cap)
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

    @app.post("/c/{modulo}/{cap}/codigo", status_code=204)
    def guardar_codigo(modulo: str, cap: str, codigo: Annotated[str, Form()]) -> Response:
        c = buscar(modulo, cap)
        progreso.guardar_codigo(c.id, codigo)
        return Response(status_code=204)

    @app.post("/c/{modulo}/{cap}/tests", response_class=HTMLResponse)
    async def ejecutar_tests(
        request: Request, modulo: str, cap: str, codigo: Annotated[str, Form()]
    ) -> HTMLResponse:
        c = buscar(modulo, cap)
        resultado = await run_in_threadpool(correr_tests, codigo, c.archivos_de_soporte())
        progreso.registrar_tests(c.id, codigo, resultado.aprobado)
        return plantillas.TemplateResponse(
            request,
            "_tests_resultado.html",
            {"cap": c, "resultado": resultado, "estado": progreso.estado(c.id)},
        )

    @app.get("/c/{modulo}/{cap}/solucion", response_class=HTMLResponse)
    def ver_solucion(modulo: str, cap: str) -> HTMLResponse:
        c = buscar(modulo, cap)
        if not progreso.estado(c.id).tests_ok:
            return HTMLResponse(
                '<p class="aviso">La solución se habilita cuando pasan todos los tests.</p>'
            )
        return HTMLResponse(str(render.codigo_html(c.solucion())))

    @app.get("/c/{modulo}/{cap}/inicial", response_class=PlainTextResponse)
    def codigo_inicial(modulo: str, cap: str) -> str:
        return buscar(modulo, cap).codigo_inicial()

    return app


app = crear_app()
