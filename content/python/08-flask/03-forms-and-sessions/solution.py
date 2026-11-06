from flask import Flask, abort, flash, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "solo-para-el-curso"

TAREAS: list[dict[str, object]] = []

PLANTILLA = """
{% for m in get_flashed_messages() %}<p class="flash">{{ m }}</p>{% endfor %}
{% for e in errores %}<p class="error">{{ e }}</p>{% endfor %}
<ul>{% for t in tareas %}<li id="t{{ t.id }}">{{ t.titulo }}</li>{% endfor %}</ul>
<form method="post"><input name="titulo" value="{{ titulo }}"></form>
"""

TEMAS = {"claro", "oscuro"}


def render(errores: list[str] | None = None, titulo: str = "") -> str:
    return render_template_string(PLANTILLA, tareas=TAREAS, errores=errores or [], titulo=titulo)


@app.get("/tareas")
def lista():
    return render()


@app.post("/tareas")
def crear():
    titulo = request.form.get("titulo", "").strip()
    errores = []
    if not titulo:
        errores.append("El título es obligatorio")
    elif len(titulo) > 50:
        errores.append("Máximo 50 caracteres")
    if errores:
        return render(errores, titulo), 400
    siguiente = max((int(t["id"]) for t in TAREAS), default=0) + 1
    TAREAS.append({"id": siguiente, "titulo": titulo})
    flash("Tarea creada")
    return redirect(url_for("lista"), code=303)


@app.post("/tareas/<int:id>/borrar")
def borrar(id: int):
    tarea = next((t for t in TAREAS if t["id"] == id), None)
    if tarea is None:
        abort(404)
    TAREAS.remove(tarea)
    flash("Tarea borrada")
    return redirect(url_for("lista"), code=303)


@app.post("/preferencias")
def guardar_preferencias():
    tema = request.form.get("tema", "")
    if tema not in TEMAS:
        abort(400)
    session["tema"] = tema
    return "", 204


@app.get("/preferencias")
def ver_preferencias():
    return {"tema": session.get("tema", "claro")}
