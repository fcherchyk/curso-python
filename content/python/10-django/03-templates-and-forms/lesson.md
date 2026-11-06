# Templates and forms

Django ships its own **template language** and a **forms** system that validates data, generates
HTML and displays errors, all integrated with **CSRF** protection. It's the part of Django that
saves the most time in apps with lots of data-entry screens.

## The template language

It's very similar to Jinja2, but deliberately more limited. The idea is that logic stays in the
view and not in the template.

```django
{% extends "base.html" %}
{% block content %}
  <h1>{{ product.name|upper }}</h1>
  <p>{{ product.price|floatformat:2 }}</p>

  {% if products %}
    {% for p in products %}
      <li>{{ forloop.counter }}. {{ p.name }}</li>
    {% empty %}
      <li>No products</li>
    {% endfor %}
  {% endif %}

  <a href="{% url 'detail' product.id %}">View</a>
  {{ messages|length }} message{{ messages|length|pluralize }}
{% endblock %}
```

Differences from Jinja2:

- Functions **can't be called with arguments** in the template: `{{ p.price_with_tax }}` works
  if it's a method with no arguments or a property, but `{{ p.price(2) }}` doesn't exist.
- Filters take **one** argument with `:`, as in `{{ text|truncatechars:30 }}`.
- `{% empty %}` inside the `for` covers the empty list, and `forloop.counter` is the index.
- `{% url 'name' args %}` reverses URLs, and `{% static 'css/app.css' %}` builds the paths to
  static files.
- **Autoescape** is on: `{{ x }}` escapes HTML. Use `|safe` or `{% autoescape off %}` only with
  trusted content.

### Rendering from a view

```python
from django.shortcuts import render, redirect, get_object_or_404

def detail(request, id):
    product = get_object_or_404(Product, id=id)          # 404 if it doesn't exist
    return render(request, "catalog/detail.html", {"product": product})
```

`render` looks for the template in the apps' `templates/` folders and in those of `TEMPLATES["DIRS"]`,
and passes it the `request` (needed for CSRF and for `request.user`). The convention is
`templates/<app>/file.html`, to avoid name clashes between apps.

## Forms: `forms.Form`

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, min_length=10)

    def clean_name(self):                      # validate/clean ONE field: clean_<field>
        return self.cleaned_data["name"].strip().title()

    def clean(self):                           # rules across fields
        data = super().clean()
        if "spam" in data.get("message", "").lower():
            raise forms.ValidationError("The message looks like spam")
        return data
```

- Each field validates its type and its constraints (`max_length`, `min_length`, `required`, email…).
- `clean_<field>` validates or transforms one field and returns the cleaned value.
- `clean()` validates rules involving several fields. Its errors are *non-field errors*.
- `form.is_valid()` runs everything. Afterwards, `form.cleaned_data` holds the cleaned data and
  `form.errors`, the errors per field.

It's the same idea as Pydantic (types, constraints and validators), with the bonus that the
form knows **how to render itself as HTML**.

### The form view pattern

```python
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)           # form "bound" to the data
        if form.is_valid():
            save(form.cleaned_data)
            return redirect("thanks")              # PRG: redirect by URL name
    else:
        form = ContactForm()                       # empty form
    return render(request, "contact.html", {"form": form})
```

If the POST doesn't validate, you re-render **the same form**, which already has the values filled
in and the errors. In the template, `{{ field }}`, `{{ field.errors }}` and `{{ form.non_field_errors }}`
do the rest.

### `ModelForm`: forms from models

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category"]

form = ProductForm(request.POST)
if form.is_valid():
    product = form.save()              # creates (or updates, with instance=...) the object
```

The fields, types and validation come from the model. Combined with the generic views in the
next chapter, a full CRUD takes very few lines.

## CSRF: why Django rejects your POSTs

*Cross-Site Request Forgery*: another site makes your user's browser send a POST to your app,
and the session cookies go along with it. Django prevents this by requiring a secret **token** on
every POST:

```django
<form method="post">
  {% csrf_token %}           ← a hidden input with the token
  ...
</form>
```

`CsrfViewMiddleware` rejects POSTs without the correct token with **403**. That's why you have to
render with `render(request, ...)`, which gives access to the token. For APIs with tokens in
headers (no cookies), DRF handles the exemption.

## Testing forms

```python
def test_form():
    form = ContactForm(data={"name": "alice", "email": "x", "message": "hi"})
    assert not form.is_valid()
    assert "email" in form.errors
```

The test `Client` does **not** check CSRF unless you ask for it with `Client(enforce_csrf_checks=True)`.

## In other frameworks

- **Flask**: Jinja2, and validation by hand or with Flask-WTF (WTForms + CSRF).
- **FastAPI**: Pydantic validates, but doesn't render forms; it's designed for APIs.

## Summary

- Templates: `{{ }}` and `{% %}`, filters with `|filter:arg`, `{% empty %}`, `{% url %}` and autoescape.
- `render(request, template, context)`, `redirect("name")` and `get_object_or_404`.
- `forms.Form`: fields with constraints, `clean_<field>` and `clean()`; `is_valid()` and
  `cleaned_data`.
- The GET/POST pattern with PRG; `ModelForm` for model forms.
- `{% csrf_token %}` in every POST form; without the token, 403.

## Exercise

The templates are in `templates/` (with `{% csrf_token %}` and error display). Write the
contact form with its validations and the views using the Post/Redirect/Get pattern.

**Further reading:** [The Django template language](https://docs.djangoproject.com/en/stable/ref/templates/language/),
[Working with forms](https://docs.djangoproject.com/en/stable/topics/forms/),
[CSRF protection](https://docs.djangoproject.com/en/stable/ref/csrf/).
