# Django: arquitectura, URLs y vistas

Django es el framework "con baterías incluidas": trae ORM, migraciones, admin, formularios,
autenticación, plantillas, caché, internacionalización y seguridad, todo integrado y con
convenciones fuertes. Donde Flask te deja elegir cada pieza y FastAPI se especializa en APIs,
Django te da **una forma de hacer todo**. Es ideal para aplicaciones grandes con mucho modelo de
datos y un backoffice.

## Proyecto y apps

```bash
uv add django
uv run django-admin startproject tienda .       # el PROYECTO: configuración global
uv run python manage.py startapp catalogo        # una APP: una funcionalidad
uv run python manage.py runserver                # http://127.0.0.1:8000
```

```
tienda/
├── manage.py               ← CLI del proyecto (runserver, migrate, shell, test…)
├── tienda/
│   ├── settings.py         ← TODA la configuración
│   └── urls.py             ← URLs raíz
└── catalogo/               ← una app
    ├── models.py           ← modelos (ORM)
    ├── views.py            ← vistas
    ├── urls.py             ← URLs de la app (lo creás vos)
    ├── admin.py            ← registro en el admin
    ├── templates/catalogo/ ← plantillas
    └── tests.py
```

Un **proyecto** contiene varias **apps**, que se activan en `INSTALLED_APPS`. Una app agrupa
modelos, vistas y URLs de un área (catálogo, pedidos, usuarios) y se puede reutilizar.

> En los ejercicios del curso no hay un proyecto completo: los tests configuran Django con
> `settings.configure(...)` y tu `ejercicio.py` hace de `urls.py`, `views.py` y `models.py`. El
> código que escribís es el mismo que irías repartiendo en esos archivos.

## MTV: Model, Template, View

Django llama a su arquitectura **MTV**:

- **Model**: los datos y su lógica (ORM).
- **Template**: la presentación (HTML).
- **View**: recibe el request, usa los modelos y devuelve una respuesta. Cumple el rol del
  "controller" de MVC.

## Vistas de función

Una vista es una función que **recibe `request`** (explícito, no global como en Flask) y
**devuelve un `HttpResponse`**:

```python
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_http_methods

def inicio(request):
    return HttpResponse("Hola, Django")

def detalle(request, id: int):
    producto = PRODUCTOS.get(id)
    if producto is None:
        raise Http404("producto inexistente")      # se levanta, como en FastAPI
    return JsonResponse(producto)

@require_http_methods(["GET", "POST"])             # otro método → 405
def productos(request):
    if request.method == "POST":
        datos = json.loads(request.body)
        ...
        return JsonResponse(nuevo, status=201)
    return JsonResponse(list(PRODUCTOS.values()), safe=False)   # safe=False para listas
```

El request tiene `request.method`, `request.GET` (query string), `request.POST` (formulario),
`request.body` (el body crudo, por ejemplo JSON), `request.headers`, `request.user` y
`request.session`.

`JsonResponse` exige un dict. Para devolver una lista hace falta `safe=False`, una protección
heredada contra un viejo ataque de JSON hijacking.

## URLs: `urlpatterns`

```python
# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("productos/", views.productos, name="productos"),
    path("productos/<int:id>/", views.detalle, name="detalle"),
    path("saludo/<str:nombre>/", views.saludo, name="saludo"),
]

# tienda/urls.py (raíz)
from django.urls import include, path
urlpatterns = [path("catalogo/", include("catalogo.urls")), path("admin/", admin.site.urls)]
```

- Converters: `str`, `int`, `slug`, `uuid` y `path`. Si no matchea, **404**.
- Convención: las rutas **terminan en `/`**. Con `APPEND_SLASH`, Django redirige `/productos` →
  `/productos/`.
- `include` arma la jerarquía de URLs por app, como los blueprints y routers.
- `name=` permite **invertir** la URL: `reverse("detalle", args=[3])` → `"/productos/3/"`, y en
  plantillas `{% url 'detalle' 3 %}`. Nunca escribas URLs a mano.

## CSRF y APIs

Django protege por defecto los POST de formularios contra **CSRF** (lo vemos con formularios).
Para un endpoint JSON que no usa cookies de sesión, se marca con `@csrf_exempt`. Para APIs en
serio, Django REST Framework maneja todo eso (capítulo 5). El cliente de testing **no** chequea
CSRF por defecto.

## Testear con el `Client`

```python
from django.test import Client

def test_detalle():
    c = Client()
    r = c.get("/productos/1/")
    assert r.status_code == 200
    assert r.json()["nombre"] == "yerba"
    r = c.post("/productos/", data={"nombre": "té"}, content_type="application/json")
```

Con `content_type="application/json"`, el `data` se manda como JSON. Sin eso, se manda como
formulario.

## Comparación

| Concepto        | Flask                     | FastAPI                    | Django                                 |
|-----------------|---------------------------|----------------------------|----------------------------------------|
| Request         | `request` global          | parámetros tipados         | primer argumento `request`             |
| Rutas           | decorador en la vista     | decorador en la vista      | lista `urlpatterns` separada            |
| 404             | `abort(404)`              | `raise HTTPException(404)` | `raise Http404`                         |
| JSON            | devolver un dict          | devolver un dict o modelo  | `JsonResponse(...)`                     |
| Nombre de URL   | nombre de la función      | nombre de la función       | `name=` en `path`                       |
| Configuración   | `app.config`              | `Settings` / dependencias  | `settings.py`                           |

## Resumen

- Un proyecto con varias apps; `settings.py` centraliza la configuración y `manage.py` es la CLI.
- MTV: los modelos, las plantillas y las vistas (funciones `request → HttpResponse`).
- `urlpatterns` con `path(ruta, vista, name=...)`, converters e `include` para las apps.
- `raise Http404`, `JsonResponse` (con `safe=False` para listas) y `@require_http_methods`.
- `reverse("nombre")` en lugar de escribir URLs a mano; `django.test.Client` para testear.

## Ejercicio

Las vistas y las URLs de un catálogo en memoria: texto, saludo, listado y alta en JSON, detalle
con 404, métodos restringidos y URLs con nombre.

**Para profundizar:** [Writing your first Django app](https://docs.djangoproject.com/en/stable/intro/tutorial01/),
[URL dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/),
[Request and response objects](https://docs.djangoproject.com/en/stable/ref/request-response/).
