"""Forms, redirects and sessions.

Routes to implement:

GET  /tasks                   → render TEMPLATE with the tasks (and the flashed messages).
POST /tasks                   → form field "title" (with surrounding whitespace stripped):
                                - empty → 400, re-render with errors=["Title is required"]
                                - more than 50 characters → 400, errors=["50 characters max"]
                                - ok → append {"id": next id, "title": ...},
                                  flash("Task created") and redirect 303 to /tasks
POST /tasks/<int:id>/delete   → if it doesn't exist, 404 (abort); if it does, delete it,
                                flash("Task deleted") and redirect 303 to /tasks
POST /preferences             → field "theme": "light" or "dark" (any other value → 400);
                                store it in session["theme"] and respond 204
GET  /preferences             → JSON {"theme": <session value or "light">}

Use url_for("task_list") for the redirect (the GET /tasks view must be called `task_list`).
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
app.secret_key = "course-only"

TASKS: list[dict[str, object]] = []

TEMPLATE = """
{% for m in get_flashed_messages() %}<p class="flash">{{ m }}</p>{% endfor %}
{% for e in errors %}<p class="error">{{ e }}</p>{% endfor %}
<ul>{% for t in tasks %}<li id="t{{ t.id }}">{{ t.title }}</li>{% endfor %}</ul>
<form method="post"><input name="title" value="{{ title }}"></form>
"""


def render(errors: list[str] | None = None, title: str = "") -> str:
    """Helper: renders TEMPLATE with the current tasks."""
    return render_template_string(
        TEMPLATE, tasks=TASKS, errors=errors or [], title=title
    )
