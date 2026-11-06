# Plantillas con Jinja2

Cuando una app devuelve páginas HTML (y no solo JSON), mezclar HTML con código Python en
strings se vuelve inmanejable enseguida. Flask usa **Jinja2**, el motor de plantillas que
también usan Ansible, dbt y esta misma app del curso. Separa la presentación de la lógica,
**escapa el HTML automáticamente** y permite herencia de plantillas.

## Renderizar una plantilla

```
mi_app/
├── app.py
└── templates/          ← Flask busca acá por defecto
    ├── base.html
    └── lista.html
```

```python
from flask import render_template

@app.get("/productos")
def lista():
    productos = buscar_productos()
    return render_template("lista.html", productos=productos, titulo="Catálogo")
```

Los argumentos con nombre son las **variables de contexto** que ve la plantilla. Además,
Flask inyecta `request`, `session`, `g` y la función `url_for`.

## La sintaxis

```jinja
{{ expresion }}                 → imprime (escapado)
{% sentencia %}                 → lógica: if, for, block, extends, set…
{# comentario #}

{{ producto.nombre }}           → atributo O clave de dict: funciona con los dos
{{ productos | length }}        → filtros con |
{{ nombre | default("anónimo") | upper }}

{% if usuario %}Hola, {{ usuario.nombre }}{% else %}Iniciá sesión{% endif %}

{% for p in productos %}
  {{ loop.index }}. {{ p.nombre }}
{% else %}
  No hay productos          ← corre si la lista está vacía
{% endfor %}
```

`loop.index`, `loop.first`, `loop.last` y `loop.length` están disponibles dentro de un `for`.

## Herencia: una plantilla base

```jinja
{# base.html #}
<html>
<head><title>{% block titulo %}Tienda{% endblock %}</title></head>
<body>
  <nav>...</nav>
  <main>{% block contenido %}{% endblock %}</main>
</body>
</html>
```

```jinja
{# lista.html #}
{% extends "base.html" %}
{% block titulo %}Productos{% endblock %}
{% block contenido %}
  <h1>Productos</h1>
  ...
{% endblock %}
```

La hija **reemplaza** los bloques que define y hereda el resto. Así el layout se escribe una
sola vez. Para incluir fragmentos, `{% include "parcial.html" %}`; para componentes con
parámetros, `{% macro %}`.

## Autoescape: la defensa contra XSS

Flask activa el **autoescape** para las plantillas `.html`: todo lo que imprimís con `{{ }}` se
escapa.

```python
nombre = '<script>alert("hack")</script>'
```
```jinja
<p>{{ nombre }}</p>
→ <p>&lt;script&gt;alert(&#34;hack&#34;)&lt;/script&gt;</p>
```

Si un usuario carga un nombre con HTML malicioso, se muestra como texto y no se ejecuta. Solo
desactivás el escape (`{{ html | safe }}` o `Markup(...)`) para HTML que **vos** generaste y
sabés que es seguro.

## `url_for`: nunca escribas URLs a mano

```jinja
<a href="{{ url_for('detalle', id=p.id) }}">{{ p.nombre }}</a>
```
```python
redirect(url_for("lista"))
```

`url_for` recibe el **nombre del endpoint** (por defecto, el nombre de la función de la vista)
y arma la URL. Si cambiás la ruta, los links se actualizan solos. Los parámetros que no son
parte de la ruta se agregan como query string.

## Filtros propios

```python
@app.template_filter("pesos")
def formatear_pesos(monto: float) -> str:
    return "$ " + f"{monto:,.2f}".translate(str.maketrans(",.", ".,"))
```
```jinja
{{ producto.precio | pesos }}     → $ 3.500,00
```

También `@app.context_processor`, para inyectar variables en todas las plantillas (por
ejemplo, el usuario actual o el año).

## Plantillas en strings

Para algo chico, `render_template_string("<p>Hola {{ nombre }}</p>", nombre=n)`. También
autoescapa. Nunca construyas una plantilla concatenando datos del usuario en el **texto de la
plantilla**: eso es *server-side template injection*. Los datos siempre van como variables.

## En los otros frameworks

- **Django** tiene su propio lenguaje de plantillas, muy parecido pero más restringido
  (no permite llamar funciones con argumentos), y también autoescapa.
- **FastAPI** está pensado para APIs, pero puede usar Jinja2 con
  `fastapi.templating.Jinja2Templates`, como esta app.

## Resumen

- `render_template("x.html", var=valor)` busca en `templates/`.
- `{{ }}` imprime escapado, `{% %}` para la lógica y `|` para los filtros.
- La herencia con `extends` y `block` evita repetir el layout.
- El autoescape previene XSS; `| safe` solo para HTML de confianza.
- `url_for("endpoint", ...)` para todos los links; `@app.template_filter` para tus filtros.

## Ejercicio

Las plantillas ya están en `templates/` (`base.html`, `lista.html` y `detalle.html`, cuyo
contenido está más abajo). Vos escribís las vistas que las renderizan, el filtro `pesos` que
usan y un saludo con `render_template_string` que tiene que escapar el HTML.

```jinja
{# lista.html #}
{% for p in productos %}
  <li><a href="{{ url_for('detalle', id=p.id) }}">{{ p.nombre }}</a> · {{ p.precio | pesos }}</li>
{% else %}
  <li>No hay productos</li>
{% endfor %}

{# detalle.html #}
<h1>{{ producto.nombre }}</h1>
<p class="precio">{{ producto.precio | pesos }}</p>
```

**Para profundizar:** [Jinja Template Designer Documentation](https://jinja.palletsprojects.com/en/stable/templates/),
[Flask: Templates](https://flask.palletsprojects.com/en/stable/templating/).
