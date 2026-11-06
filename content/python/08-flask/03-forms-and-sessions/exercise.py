"""Formularios, redirecciones y sesiones.

Rutas a implementar:

GET  /tareas                  → render de PLANTILLA con las tareas (y los flash).
POST /tareas                  → campo de formulario "titulo" (sin espacios alrededor):
                                - vacío → 400, re-render con errores=["El título es obligatorio"]
                                - más de 50 caracteres → 400, errores=["Máximo 50 caracteres"]
                                - ok → se agrega {"id": siguiente id, "titulo": ...},
                                  flash("Tarea creada") y redirect 303 a /tareas
POST /tareas/<int:id>/borrar  → si no existe, 404 (abort); si existe, se borra,
                                flash("Tarea borrada") y redirect 303 a /tareas
POST /preferencias            → campo "tema": "claro" u "oscuro" (otro valor → 400);
                                lo guarda en session["tema"] y responde 204
GET  /preferencias            → JSON {"tema": <session o "claro">}

Usá url_for("lista") para el redirect (la vista de GET /tareas se tiene que llamar `lista`).
"""

from flask import (  # noqa: F401
    Flask,
    abort,
    flash,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = "solo-para-el-curso"

TAREAS: list[dict[str, object]] = []

PLANTILLA = """
{% for m in get_flashed_messages() %}<p class="flash">{{ m }}</p>{% endfor %}
{% for e in errores %}<p class="error">{{ e }}</p>{% endfor %}
<ul>{% for t in tareas %}<li id="t{{ t.id }}">{{ t.titulo }}</li>{% endfor %}</ul>
<form method="post"><input name="titulo" value="{{ titulo }}"></form>
"""


def render(errores: list[str] | None = None, titulo: str = "") -> str:
    """Helper: renderiza PLANTILLA con las tareas actuales."""
    return render_template_string(
        PLANTILLA, tareas=TAREAS, errores=errores or [], titulo=titulo
    )
