# Forms, redirects and sessions

Classic web apps (the ones that return HTML, not an SPA) run on a simple cycle: the browser
submits a **form** with POST, the server validates and saves, and then **redirects** to another
page. Three tools show up along the way: **flash** messages, the user's **session** and `abort`
for HTTP errors.

## Reading a form

```html
<form method="post" action="/tasks">
  <input name="title">
  <button>Add</button>
</form>
```

```python
from flask import request

@app.post("/tasks")
def create():
    title = request.form.get("title", "").strip()
    ...
```

- `request.form` is a dict of the fields sent as `application/x-www-form-urlencoded` or
  `multipart/form-data`.
- `request.form["x"]` raises a 400 error if the field is missing; `.get("x", default)` doesn't.
- `request.form.getlist("tags")` for repeated fields (checkboxes).
- Uploaded files arrive in `request.files`.

## Validating: never trust the client

Browser validation (`required`, `maxlength`) is for the user experience. **Real validation
happens on the server**, because anyone can send a POST with `curl`.

If the data is invalid, the usual move is to **show the form again** with the errors and the
values the user already typed, with status **400** (or 422):

```python
errors = []
if not title:
    errors.append("Title is required")
if errors:
    return render_template("tasks.html", errors=errors, title=title), 400
```

For big forms there are extensions that declare the fields and their rules, like **Flask-WTF**
(WTForms), which also adds **CSRF** protection. Django has the same built in with its `Form`.

## The Post/Redirect/Get (PRG) pattern

```python
from flask import redirect, url_for

@app.post("/tasks")
def create():
    ...                                   # validate and save
    return redirect(url_for("task_list"), code=303)
```

If you returned HTML directly after a successful POST, pressing F5 would make the browser
**resubmit the form** (the infamous "Confirm form resubmission?"), and you'd create the task
twice. With a redirect, the final page is a GET, which is safe to reload.

- **302/303**: redirect after a POST. 303 makes it explicit that the next request is a GET.
- **301/308**: permanent redirect (the URL changed for good).

## Flash messages: notifying after the redirect

How do you show "Task created" if you redirect after the POST? With a **flash**: a message stored
in the session and consumed **only once**, on the next request.

```python
from flask import flash, get_flashed_messages

flash("Task created")                 # in the POST view
flash("Couldn't delete", "error")     # with a category
```
```jinja
{% for message in get_flashed_messages() %}
  <p class="notice">{{ message }}</p>
{% endfor %}
```

## The session

`session` is a per-user dict that **persists across requests**:

```python
from flask import session

app.secret_key = "change-in-production"      # required to use session and flash

session["theme"] = "dark"
theme = session.get("theme", "light")
session.pop("cart", None)
session.clear()                               # logout
```

By default, Flask stores the session **in a signed cookie**:

- **Signed is not encrypted**: users can *read* its contents (it's base64), but they can't change
  it without breaking the signature. **Don't store secrets there.**
- The signature depends on `secret_key`: if it leaks, anyone can forge valid sessions. In
  production it comes from an environment variable and is long and random.
- For large or server-side sessions, use the Flask-Session extension.

## `abort`: bailing out with an HTTP error

```python
from flask import abort

task = find(id)
if task is None:
    abort(404)
if task.owner != current_user:
    abort(403)
```

`abort` raises an HTTP exception that Flask turns into the error response. You can customize it
with `@app.errorhandler(404)` (upcoming chapters).

## Testing it

```python
def test_create_redirects_and_notifies(client):
    r = client.post("/tasks", data={"title": "buy coffee"})
    assert r.status_code == 303
    r = client.get(r.headers["Location"])         # or follow_redirects=True
    assert "Task created" in r.text
```

`data=` sends a form (and `json=` sends JSON). The test client **keeps cookies** between
requests, so the session and flash messages work just like in a browser.

## In the other frameworks

| Flask                       | Django                                 | FastAPI                               |
|-----------------------------|----------------------------------------|---------------------------------------|
| `request.form`              | `request.POST` + `forms.Form`           | `Form(...)` in the parameters         |
| `flash()`                   | `messages.success(request, ...)`        | not built in: roll your own with cookies |
| `session` (signed cookie)   | `request.session` (database by default) | Starlette's `SessionMiddleware`       |
| `redirect(url_for(...))`    | `redirect("url-name")`                  | `RedirectResponse(...)`               |
| CSRF with Flask-WTF         | built-in CSRF                           | by hand or with a library             |

## Summary

- `request.form` to read forms; always validate on the server and return 400 with the errors.
- Post/Redirect/Get: after a successful POST, `redirect(..., code=303)`.
- `flash` for one-time messages; `session` for per-user state (signed cookie, not encrypted).
- `secret_key` is required, secret and kept out of the code.
- `abort(404)` or `abort(403)` to bail out with an error.

## Exercise

A task list with validated creation, PRG with flash, deletion with 404 and preferences stored in
the session. The templates come as strings in the starter code.

**Further reading:** [Flask: Sessions](https://flask.palletsprojects.com/en/stable/quickstart/#sessions),
[Message Flashing](https://flask.palletsprojects.com/en/stable/patterns/flashing/),
[Post/Redirect/Get](https://en.wikipedia.org/wiki/Post/Redirect/Get).
