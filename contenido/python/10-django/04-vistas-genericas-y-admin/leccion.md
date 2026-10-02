# Vistas basadas en clases y el admin

Los listados, los detalles, las altas, las ediciones y los borrados se repiten en casi toda app.
Django los resuelve con **vistas genéricas basadas en clases** (CBV): heredás de `ListView`,
`DetailView` o `CreateView`, configurás dos o tres atributos y listo. Y para la gestión interna
de los datos trae algo único entre los frameworks: el **admin**, un backoffice completo que se
genera a partir de tus modelos.

## De función a clase

```python
# Vista de función
def lista(request):
    libros = Libro.objects.order_by("titulo")
    return render(request, "libros/lista.html", {"libros": libros})

# La misma vista, genérica
from django.views.generic import ListView

class LibroLista(ListView):
    model = Libro
    ordering = ["titulo"]
    template_name = "libros/lista.html"
    context_object_name = "libros"
```

```python
urlpatterns = [path("libros/", LibroLista.as_view(), name="lista")]
```

`as_view()` convierte la clase en una función de vista. Cada request crea una instancia nueva:
nada de estado compartido.

## Las genéricas principales

| Clase          | Para qué                        | Atributos clave                               |
|----------------|---------------------------------|-----------------------------------------------|
| `ListView`     | listado (con paginación)        | `model`, `queryset`, `ordering`, `paginate_by` |
| `DetailView`   | un objeto por `pk` o `slug`     | `model`, `context_object_name`                |
| `CreateView`   | formulario de alta              | `model`, `fields`, `success_url`              |
| `UpdateView`   | formulario de edición           | ídem                                          |
| `DeleteView`   | confirmación y borrado          | `success_url`                                 |
| `TemplateView` | una plantilla estática          | `template_name`                               |
| `RedirectView` | redirección                     | `url` o `pattern_name`                        |

Sin `template_name`, Django busca `<app>/<modelo>_list.html`, `<app>/<modelo>_detail.html` o
`<app>/<modelo>_form.html`.

### Personalizar: sobrescribir métodos

Las CBV están armadas con métodos que se pueden sobrescribir:

```python
class LibroLista(ListView):
    model = Libro
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        if q := self.request.GET.get("q"):
            qs = qs.filter(titulo__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["busqueda"] = self.request.GET.get("q", "")
        return contexto
```

- `get_queryset()` decide **qué objetos** se muestran: filtros, búsqueda o solo los del usuario.
- `get_context_data()` agrega variables a la plantilla.
- `self.request`, `self.kwargs` (los parámetros de la URL) y `self.object` están disponibles.
- Con `paginate_by`, la plantilla recibe `page_obj` y `paginator`, y la página se elige con
  `?page=2`.

### Crear con validación incluida

```python
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class LibroCrear(CreateView):
    model = Libro
    fields = ["titulo", "autor", "anio"]          # arma un ModelForm por vos
    template_name = "libros/form.html"
    success_url = reverse_lazy("lista")           # adónde redirigir después de guardar
```

GET muestra el formulario; POST valida, guarda y redirige (PRG); y si es inválido, vuelve a
mostrar el form con errores. Es todo el patrón del capítulo anterior en cinco líneas.
`reverse_lazy` en lugar de `reverse`, porque al definir la clase las URLs todavía no están
cargadas.

Para comportamientos transversales existen los **mixins**: `LoginRequiredMixin` (próximo
capítulo), `PermissionRequiredMixin` y los tuyos propios.

### ¿Funciones o clases?

Las CBV brillan en el CRUD estándar. Para lógica muy particular, una vista de función suele ser
más clara: no hay que conocer qué métodos sobrescribir. Las dos son idiomáticas.

## El admin

```python
from django.contrib import admin

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ["titulo", "autor", "anio"]       # columnas del listado
    search_fields = ["titulo", "autor"]               # caja de búsqueda
    list_filter = ["anio"]                            # filtros laterales
    ordering = ["titulo"]
    list_per_page = 50
```

```bash
uv run python manage.py createsuperuser
# → http://127.0.0.1:8000/admin/
```

Con eso tenés listado, búsqueda, filtros, alta, edición, borrado, historial y permisos por
usuario, sin escribir ni una plantilla. Se puede personalizar mucho más: `readonly_fields`,
`inlines` para editar relacionados en la misma pantalla, acciones en lote con `actions`, etc.

El admin está pensado para el **equipo interno**, no para los usuarios finales de tu producto.

## En los otros frameworks

- **Flask**: no hay CBV equivalentes (existen `MethodView`), y el admin se consigue con
  Flask-Admin.
- **FastAPI**: los routers y las dependencias cumplen ese rol para APIs; para un panel, librerías
  como SQLAdmin.

Ninguno trae algo tan completo como el admin de Django, y es una de las razones más fuertes
para elegirlo.

## Resumen

- `ListView`, `DetailView`, `CreateView`, `UpdateView` y `DeleteView` + `as_view()`.
- Configurás atributos (`model`, `fields`, `template_name`, `paginate_by`, `success_url`) y
  sobrescribís `get_queryset`/`get_context_data` para personalizar.
- `reverse_lazy` en los atributos de clase.
- `@admin.register(Modelo)` + `ModelAdmin` (`list_display`, `search_fields`, `list_filter`) da un
  backoffice completo.

## Ejercicio

Un CRUD de libros con vistas genéricas: listado con búsqueda y paginación, detalle, alta con
redirección y el registro en el admin. Las plantillas están en `templates/libros/`.

**Para profundizar:** [Class-based views](https://docs.djangoproject.com/en/stable/topics/class-based-views/),
[Generic display views](https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/),
[The Django admin site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/),
[Classy CBV](https://ccbv.co.uk/) (referencia de todos los métodos).
