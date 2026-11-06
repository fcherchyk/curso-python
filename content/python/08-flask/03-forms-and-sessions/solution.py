from flask import Flask, abort, flash, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "course-only"

TASKS: list[dict[str, object]] = []

TEMPLATE = """
{% for m in get_flashed_messages() %}<p class="flash">{{ m }}</p>{% endfor %}
{% for e in errors %}<p class="error">{{ e }}</p>{% endfor %}
<ul>{% for t in tasks %}<li id="t{{ t.id }}">{{ t.title }}</li>{% endfor %}</ul>
<form method="post"><input name="title" value="{{ title }}"></form>
"""

THEMES = {"light", "dark"}


def render(errors: list[str] | None = None, title: str = "") -> str:
    return render_template_string(TEMPLATE, tasks=TASKS, errors=errors or [], title=title)


@app.get("/tasks")
def task_list():
    return render()


@app.post("/tasks")
def create():
    title = request.form.get("title", "").strip()
    errors = []
    if not title:
        errors.append("Title is required")
    elif len(title) > 50:
        errors.append("50 characters max")
    if errors:
        return render(errors, title), 400
    next_id = max((int(t["id"]) for t in TASKS), default=0) + 1
    TASKS.append({"id": next_id, "title": title})
    flash("Task created")
    return redirect(url_for("task_list"), code=303)


@app.post("/tasks/<int:id>/delete")
def delete(id: int):
    task = next((t for t in TASKS if t["id"] == id), None)
    if task is None:
        abort(404)
    TASKS.remove(task)
    flash("Task deleted")
    return redirect(url_for("task_list"), code=303)


@app.post("/preferences")
def save_preferences():
    theme = request.form.get("theme", "")
    if theme not in THEMES:
        abort(400)
    session["theme"] = theme
    return "", 204


@app.get("/preferences")
def show_preferences():
    return {"theme": session.get("theme", "light")}
