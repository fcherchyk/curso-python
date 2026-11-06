# Plantillas y formularios

Django trae su propio **lenguaje de plantillas** y un sistema de **formularios** que valida datos,
genera HTML y muestra errores, todo integrado con la protección **CSRF**. Es la parte de Django
que más tiempo ahorra en apps con muchas pantallas de carga de datos.

## El lenguaje de plantillas

Es muy parecido a Jinja2, pero deliberadamente más limitado. La idea es que la lógica quede en
la vista y no en la plantilla.

```django
{% extends "base.html" %}
{% block contenido %}
  <h1>{{ producto.nombre|upper }}</h1>
  <p>{{ producto.precio|floatformat:2 }}</p>

  {% if productos %}
    {% for p in productos %}
      <li>{{ forloop.counter }}. {{ p.nombre }}</li>
    {% empty %}
      <li>No hay productos</li>
    {% endfor %}
  {% endif %}

  <a href="{% url 'detalle' producto.id %}">Ver</a>
  {{ mensajes|length }} mensaje{{ mensajes|length|pluralize }}
{% endblock %}
```

Diferencias con Jinja2:

- Las funciones **no se llaman con argumentos** en la plantilla: `{{ p.precio_con_iva }}` funciona
  si es un método sin argumentos o una property, pero `{{ p.precio(2) }}` no existe.
- Los filtros reciben **un** argumento con `:`, como `{{ texto|truncatechars:30 }}`.
- `{% empty %}` dentro del `for` cubre la lista vacía, y `forloop.counter` es el índice.
- `{% url 'nombre' args %}` invierte URLs, y `{% static 'css/app.css' %}` arma las rutas de los
  estáticos.
- **Autoescape** activado: `{{ x }}` escapa el HTML. `|safe` o `{% autoescape off %}` solo con
  contenido de confianza.

### Renderizar desde una vista

```python
from django.shortcuts import render, redirect, get_object_or_404

def detalle(request, id):
    producto = get_object_or_404(Producto, id=id)        # 404 si no existe
    return render(request, "catalogo/detalle.html", {"producto": producto})
```

`render` busca la plantilla en las carpetas `templates/` de las apps y en las de `TEMPLATES["DIRS"]`,
y le pasa el `request` (necesario para CSRF y para `request.user`). La convención es
`templates/<app>/archivo.html`, para evitar choques de nombres entre apps.

## Formularios: `forms.Form`

```python
from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea, min_length=10)

    def clean_nombre(self):                    # validar/limpiar UN campo: clean_<campo>
        return self.cleaned_data["nombre"].strip().title()

    def clean(self):                           # reglas entre campos
        datos = super().clean()
        if "spam" in datos.get("mensaje", "").lower():
            raise forms.ValidationError("El mensaje parece spam")
        return datos
```

- Cada campo valida su tipo y sus restricciones (`max_length`, `min_length`, `required`, email…).
- `clean_<campo>` valida o transforma un campo y devuelve el valor limpio.
- `clean()` valida reglas que involucran varios campos. Sus errores son *non-field errors*.
- `form.is_valid()` corre todo. Después, `form.cleaned_data` tiene los datos limpios y
  `form.errors`, los errores por campo.

Es la misma idea que Pydantic (tipos, restricciones y validadores), con el agregado de que el
form sabe **dibujarse en HTML**.

### El patrón de la vista con formulario

```python
def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)          # formulario "ligado" a los datos
        if form.is_valid():
            guardar(form.cleaned_data)
            return redirect("gracias")             # PRG: redirect por nombre de URL
    else:
        form = ContactoForm()                      # formulario vacío
    return render(request, "contacto.html", {"form": form})
```

Si el POST no valida, se vuelve a renderizar **el mismo form**, que ya tiene los valores cargados
y los errores. En la plantilla, `{{ campo }}`, `{{ campo.errors }}` y `{{ form.non_field_errors }}`
hacen el resto.

### `ModelForm`: formularios a partir de modelos

```python
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "categoria"]

form = ProductoForm(request.POST)
if form.is_valid():
    producto = form.save()             # crea (o actualiza, con instance=...) el objeto
```

Los campos, los tipos y la validación salen del modelo. Combinado con las vistas genéricas del
próximo capítulo, un CRUD completo son muy pocas líneas.

## CSRF: por qué Django rechaza tus POST

*Cross-Site Request Forgery*: otro sitio hace que el navegador de tu usuario envíe un POST a tu
app, y las cookies de sesión van incluidas. Django lo evita exigiendo un **token** secreto en
cada POST:

```django
<form method="post">
  {% csrf_token %}           ← un input oculto con el token
  ...
</form>
```

El `CsrfViewMiddleware` rechaza con **403** los POST sin el token correcto. Por eso hay que
renderizar con `render(request, ...)`, que da acceso al token. Para APIs con tokens en headers
(sin cookies), DRF maneja la exención.

## Testear formularios

```python
def test_form():
    form = ContactoForm(data={"nombre": "ana", "email": "x", "mensaje": "hola"})
    assert not form.is_valid()
    assert "email" in form.errors
```

El `Client` de tests **no** chequea CSRF salvo que lo pidas con `Client(enforce_csrf_checks=True)`.

## En los otros frameworks

- **Flask**: Jinja2 y validación a mano o con Flask-WTF (WTForms + CSRF).
- **FastAPI**: Pydantic valida, pero no dibuja formularios; está pensado para APIs.

## Resumen

- Plantillas: `{{ }}` y `{% %}`, filtros con `|filtro:arg`, `{% empty %}`, `{% url %}` y autoescape.
- `render(request, plantilla, contexto)`, `redirect("nombre")` y `get_object_or_404`.
- `forms.Form`: campos con restricciones, `clean_<campo>` y `clean()`; `is_valid()` y
  `cleaned_data`.
- Patrón GET/POST con PRG; `ModelForm` para formularios de modelos.
- `{% csrf_token %}` en cada form con POST; sin el token, 403.

## Ejercicio

Las plantillas están en `templates/` (con `{% csrf_token %}` y la muestra de errores). Escribí el
formulario de contacto con sus validaciones y las vistas con el patrón Post/Redirect/Get.

**Para profundizar:** [The Django template language](https://docs.djangoproject.com/en/stable/ref/templates/language/),
[Working with forms](https://docs.djangoproject.com/en/stable/topics/forms/),
[CSRF protection](https://docs.djangoproject.com/en/stable/ref/csrf/).
