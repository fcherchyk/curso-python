# Formularios, redirecciones y sesiones

Las apps web clásicas (las que devuelven HTML, no una SPA) funcionan con un ciclo simple: el
navegador envía un **formulario** con POST, el servidor valida y guarda y después **redirige**
a otra página. En el medio aparecen tres herramientas: los mensajes **flash**, la **sesión**
del usuario y `abort` para los errores HTTP.

## Leer un formulario

```html
<form method="post" action="/tareas">
  <input name="titulo">
  <button>Agregar</button>
</form>
```

```python
from flask import request

@app.post("/tareas")
def crear():
    titulo = request.form.get("titulo", "").strip()
    ...
```

- `request.form` es un dict de los campos enviados con `application/x-www-form-urlencoded` o
  `multipart/form-data`.
- `request.form["x"]` levanta un error 400 si falta el campo; `.get("x", default)` no.
- `request.form.getlist("tags")` para campos repetidos (checkboxes).
- Los archivos subidos llegan en `request.files`.

## Validar: nunca confíes en el cliente

La validación del navegador (`required`, `maxlength`) es para la experiencia de uso. **La
validación real va en el servidor**, porque cualquiera puede mandar un POST con `curl`.

Si los datos son inválidos, lo habitual es **volver a mostrar el formulario** con los errores y
los valores que el usuario ya cargó, con status **400** (o 422):

```python
errores = []
if not titulo:
    errores.append("El título es obligatorio")
if errores:
    return render_template("tareas.html", errores=errores, titulo=titulo), 400
```

Para formularios grandes existen extensiones que declaran los campos y sus reglas, como
**Flask-WTF** (WTForms), que además agrega protección **CSRF**. Django trae lo mismo
incorporado con sus `Form`.

## El patrón Post/Redirect/Get (PRG)

```python
from flask import redirect, url_for

@app.post("/tareas")
def crear():
    ...                                   # validar y guardar
    return redirect(url_for("lista"), code=303)
```

Si después de un POST exitoso devolvieras HTML directamente, al apretar F5 el navegador
**reenviaría el formulario** (el famoso "¿Confirmar reenvío?"), y crearías la tarea dos veces.
Redirigiendo, la página final es un GET, que se puede recargar sin riesgo.

- **302/303**: redirección después de un POST. 303 deja explícito que el siguiente request es un
  GET.
- **301/308**: redirección permanente (la URL cambió para siempre).

## Mensajes flash: avisar después del redirect

¿Cómo mostrás "Tarea creada" si después del POST redirigís? Con un **flash**: un mensaje que se
guarda en la sesión y se consume **una sola vez**, en el próximo request.

```python
from flask import flash, get_flashed_messages

flash("Tarea creada")                 # en la vista del POST
flash("No se pudo borrar", "error")   # con categoría
```
```jinja
{% for mensaje in get_flashed_messages() %}
  <p class="aviso">{{ mensaje }}</p>
{% endfor %}
```

## La sesión

`session` es un dict por usuario que **persiste entre requests**:

```python
from flask import session

app.secret_key = "cambiar-en-produccion"     # obligatoria para usar session y flash

session["tema"] = "oscuro"
tema = session.get("tema", "claro")
session.pop("carrito", None)
session.clear()                               # logout
```

Por defecto, Flask guarda la sesión **en una cookie firmada**:

- **Firmada no es cifrada**: el usuario puede *leer* su contenido (está en base64), pero no
  modificarlo sin que la firma falle. **No guardes secretos ahí.**
- La firma depende de `secret_key`: si se filtra, cualquiera puede fabricar sesiones válidas.
  En producción viene de una variable de entorno y es larga y aleatoria.
- Para sesiones grandes o del lado del servidor, la extensión Flask-Session.

## `abort`: cortar con un error HTTP

```python
from flask import abort

tarea = buscar(id)
if tarea is None:
    abort(404)
if tarea.dueño != usuario_actual:
    abort(403)
```

`abort` levanta una excepción HTTP que Flask convierte en la respuesta de error. Se puede
personalizar con `@app.errorhandler(404)` (próximos capítulos).

## Probarlo

```python
def test_crear_redirige_y_avisa(cliente):
    r = cliente.post("/tareas", data={"titulo": "comprar yerba"})
    assert r.status_code == 303
    r = cliente.get(r.headers["Location"])        # o follow_redirects=True
    assert "Tarea creada" in r.text
```

`data=` envía un formulario (y `json=` envía JSON). El cliente de testing **guarda las
cookies** entre requests, así que la sesión y los flash funcionan como en un navegador.

## En los otros frameworks

| Flask                       | Django                                 | FastAPI                               |
|-----------------------------|----------------------------------------|---------------------------------------|
| `request.form`              | `request.POST` + `forms.Form`           | `Form(...)` en los parámetros         |
| `flash()`                   | `messages.success(request, ...)`        | no trae: se arma con cookies          |
| `session` (cookie firmada)  | `request.session` (base de datos por defecto) | `SessionMiddleware` de Starlette |
| `redirect(url_for(...))`    | `redirect("nombre-de-url")`             | `RedirectResponse(...)`               |
| CSRF con Flask-WTF          | CSRF incorporado                        | a mano o con una librería             |

## Resumen

- `request.form` para leer formularios; validá siempre en el servidor y devolvé 400 con los errores.
- Post/Redirect/Get: después de un POST exitoso, `redirect(..., code=303)`.
- `flash` para mensajes de un solo uso; `session` para estado por usuario (cookie firmada, no
  cifrada).
- `secret_key` obligatoria, secreta y fuera del código.
- `abort(404)` o `abort(403)` para cortar con un error.

## Ejercicio

Una lista de tareas con alta validada, PRG con flash, borrado con 404 y preferencias guardadas
en la sesión. Las plantillas vienen como strings en el código inicial.

**Para profundizar:** [Flask: Sessions](https://flask.palletsprojects.com/en/stable/quickstart/#sessions),
[Message Flashing](https://flask.palletsprojects.com/en/stable/patterns/flashing/),
[Post/Redirect/Get](https://en.wikipedia.org/wiki/Post/Redirect/Get).
