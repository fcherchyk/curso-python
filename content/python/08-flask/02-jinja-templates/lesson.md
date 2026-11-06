# Templates with Jinja2

When an app returns HTML pages (not just JSON), mixing HTML and Python code in strings quickly
becomes unmanageable. Flask uses **Jinja2**, the template engine also used by Ansible, dbt and
this very course app. It separates presentation from logic, **escapes HTML automatically** and
supports template inheritance.

## Rendering a template

```
my_app/
├── app.py
└── templates/          ← Flask looks here by default
    ├── base.html
    └── list.html
```

```python
from flask import render_template

@app.get("/products")
def product_list():
    products = find_products()
    return render_template("list.html", products=products, title="Catalog")
```

The keyword arguments are the **context variables** the template sees. Flask also injects
`request`, `session`, `g` and the `url_for` function.

## The syntax

```jinja
{{ expression }}                → prints (escaped)
{% statement %}                 → logic: if, for, block, extends, set…
{# comment #}

{{ product.name }}              → attribute OR dict key: works with both
{{ products | length }}         → filters with |
{{ name | default("anonymous") | upper }}

{% if user %}Hello, {{ user.name }}{% else %}Log in{% endif %}

{% for p in products %}
  {{ loop.index }}. {{ p.name }}
{% else %}
  No products               ← runs if the list is empty
{% endfor %}
```

`loop.index`, `loop.first`, `loop.last` and `loop.length` are available inside a `for`.

## Inheritance: a base template

```jinja
{# base.html #}
<html>
<head><title>{% block title %}Store{% endblock %}</title></head>
<body>
  <nav>...</nav>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

```jinja
{# list.html #}
{% extends "base.html" %}
{% block title %}Products{% endblock %}
{% block content %}
  <h1>Products</h1>
  ...
{% endblock %}
```

The child **replaces** the blocks it defines and inherits the rest. That way you write the layout
only once. To include fragments, use `{% include "partial.html" %}`; for components with
parameters, `{% macro %}`.

## Autoescaping: the defense against XSS

Flask turns on **autoescaping** for `.html` templates: everything you print with `{{ }}` gets
escaped.

```python
name = '<script>alert("hack")</script>'
```
```jinja
<p>{{ name }}</p>
→ <p>&lt;script&gt;alert(&#34;hack&#34;)&lt;/script&gt;</p>
```

If a user submits a name with malicious HTML, it shows up as text and doesn't run. Only turn
escaping off (`{{ html | safe }}` or `Markup(...)`) for HTML that **you** generated and know is
safe.

## `url_for`: never write URLs by hand

```jinja
<a href="{{ url_for('product_detail', id=p.id) }}">{{ p.name }}</a>
```
```python
redirect(url_for("product_list"))
```

`url_for` takes the **endpoint name** (by default, the name of the view function) and builds the
URL. If you change the route, the links update themselves. Parameters that aren't part of the
route are added as a query string.

## Custom filters

```python
@app.template_filter("money")
def format_money(amount: float) -> str:
    return "$ " + f"{amount:,.2f}".translate(str.maketrans(",.", ".,"))
```
```jinja
{{ product.price | money }}       → $ 3.500,00
```

There's also `@app.context_processor`, to inject variables into every template (for example, the
current user or the year).

## Templates in strings

For something small, `render_template_string("<p>Hello {{ name }}</p>", name=n)`. It autoescapes
too. Never build a template by concatenating user data into the **template text**: that's
*server-side template injection*. Data always goes in as variables.

## In the other frameworks

- **Django** has its own template language, very similar but more restricted (it doesn't let you
  call functions with arguments), and it autoescapes too.
- **FastAPI** is designed for APIs, but it can use Jinja2 via
  `fastapi.templating.Jinja2Templates`, like this app does.

## Summary

- `render_template("x.html", var=value)` looks in `templates/`.
- `{{ }}` prints escaped, `{% %}` is for logic and `|` is for filters.
- Inheritance with `extends` and `block` keeps you from repeating the layout.
- Autoescaping prevents XSS; `| safe` only for trusted HTML.
- `url_for("endpoint", ...)` for every link; `@app.template_filter` for your own filters.

## Exercise

The templates are already in `templates/` (`base.html`, `list.html` and `detail.html`, shown
below). You write the views that render them, the `money` filter they use (dot for thousands,
comma for decimals) and a greeting with `render_template_string` that must escape HTML.

```jinja
{# list.html #}
{% for p in products %}
  <li><a href="{{ url_for('product_detail', id=p.id) }}">{{ p.name }}</a> · {{ p.price | money }}</li>
{% else %}
  <li>No products</li>
{% endfor %}

{# detail.html #}
<h1>{{ product.name }}</h1>
<p class="price">{{ product.price | money }}</p>
```

**Further reading:** [Jinja Template Designer Documentation](https://jinja.palletsprojects.com/en/stable/templates/),
[Flask: Templates](https://flask.palletsprojects.com/en/stable/templating/).
