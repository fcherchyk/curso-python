# Django: architecture, URLs and views

Django is the "batteries included" framework: it ships an ORM, migrations, an admin, forms,
authentication, templates, caching, internationalization and security, all integrated and with
strong conventions. Where Flask lets you pick every piece and FastAPI specializes in APIs,
Django gives you **one way to do everything**. It's ideal for large applications with a big data
model and a back office.

## Projects and apps

```bash
uv add django
uv run django-admin startproject shop .         # the PROJECT: global configuration
uv run python manage.py startapp catalog         # an APP: one feature
uv run python manage.py runserver                # http://127.0.0.1:8000
```

```
shop/
├── manage.py               ← project CLI (runserver, migrate, shell, test…)
├── shop/
│   ├── settings.py         ← ALL the configuration
│   └── urls.py             ← root URLs
└── catalog/                ← an app
    ├── models.py           ← models (ORM)
    ├── views.py            ← views
    ├── urls.py             ← the app's URLs (you create it)
    ├── admin.py            ← admin registration
    ├── templates/catalog/  ← templates
    └── tests.py
```

A **project** contains several **apps**, which are enabled in `INSTALLED_APPS`. An app groups the
models, views and URLs of one area (catalog, orders, users) and can be reused.

> The course exercises don't have a full project: the tests configure Django with
> `settings.configure(...)` and your `exercise.py` acts as `urls.py`, `views.py` and `models.py`. The
> code you write is the same code you would spread across those files.

## MTV: Model, Template, View

Django calls its architecture **MTV**:

- **Model**: the data and its logic (ORM).
- **Template**: the presentation (HTML).
- **View**: receives the request, uses the models and returns a response. It plays the role of
  the MVC "controller".

## Function views

A view is a function that **receives `request`** (explicitly, not a global like in Flask) and
**returns an `HttpResponse`**:

```python
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_http_methods

def home(request):
    return HttpResponse("Hello, Django")

def detail(request, id: int):
    product = PRODUCTS.get(id)
    if product is None:
        raise Http404("product not found")         # raised, like in FastAPI
    return JsonResponse(product)

@require_http_methods(["GET", "POST"])             # any other method → 405
def products(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ...
        return JsonResponse(new, status=201)
    return JsonResponse(list(PRODUCTS.values()), safe=False)   # safe=False for lists
```

The request has `request.method`, `request.GET` (query string), `request.POST` (form),
`request.body` (the raw body, for example JSON), `request.headers`, `request.user` and
`request.session`.

`JsonResponse` requires a dict. To return a list you need `safe=False`, a protection inherited
from an old JSON hijacking attack.

## URLs: `urlpatterns`

```python
# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name="products"),
    path("products/<int:id>/", views.detail, name="detail"),
    path("greet/<str:name>/", views.greet, name="greet"),
]

# shop/urls.py (root)
from django.urls import include, path
urlpatterns = [path("catalog/", include("catalog.urls")), path("admin/", admin.site.urls)]
```

- Converters: `str`, `int`, `slug`, `uuid` and `path`. If nothing matches, **404**.
- Convention: routes **end in `/`**. With `APPEND_SLASH`, Django redirects `/products` →
  `/products/`.
- `include` builds the URL hierarchy per app, like blueprints and routers.
- `name=` lets you **reverse** the URL: `reverse("detail", args=[3])` → `"/products/3/"`, and in
  templates `{% url 'detail' 3 %}`. Never write URLs by hand.

## CSRF and APIs

By default Django protects form POSTs against **CSRF** (we'll see it with forms). A JSON endpoint
that doesn't use session cookies is marked with `@csrf_exempt`. For serious APIs, Django REST
Framework handles all of that (chapter 5). The test client does **not** check CSRF by default.

## Testing with the `Client`

```python
from django.test import Client

def test_detail():
    c = Client()
    r = c.get("/products/1/")
    assert r.status_code == 200
    assert r.json()["name"] == "mate"
    r = c.post("/products/", data={"name": "tea"}, content_type="application/json")
```

With `content_type="application/json"`, `data` is sent as JSON. Without it, it's sent as a
form.

## Comparison

| Concept         | Flask                     | FastAPI                    | Django                                 |
|-----------------|---------------------------|----------------------------|----------------------------------------|
| Request         | global `request`          | typed parameters           | first argument `request`               |
| Routes          | decorator on the view     | decorator on the view      | separate `urlpatterns` list            |
| 404             | `abort(404)`              | `raise HTTPException(404)` | `raise Http404`                        |
| JSON            | return a dict             | return a dict or model     | `JsonResponse(...)`                    |
| URL name        | function name             | function name              | `name=` in `path`                      |
| Configuration   | `app.config`              | `Settings` / dependencies  | `settings.py`                          |

## Summary

- One project with several apps; `settings.py` centralizes the configuration and `manage.py` is the CLI.
- MTV: models, templates and views (functions `request → HttpResponse`).
- `urlpatterns` with `path(route, view, name=...)`, converters and `include` for apps.
- `raise Http404`, `JsonResponse` (with `safe=False` for lists) and `@require_http_methods`.
- `reverse("name")` instead of writing URLs by hand; `django.test.Client` for testing.

## Exercise

The views and URLs of an in-memory catalog: plain text, a greeting, listing and creating in JSON,
a detail with 404, restricted methods and named URLs.

**Further reading:** [Writing your first Django app](https://docs.djangoproject.com/en/stable/intro/tutorial01/),
[URL dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/),
[Request and response objects](https://docs.djangoproject.com/en/stable/ref/request-response/).
