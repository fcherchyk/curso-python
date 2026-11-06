# Class-based views and the admin

Lists, details, creates, edits and deletes repeat in almost every app. Django solves them with
**generic class-based views** (CBVs): you inherit from `ListView`, `DetailView` or `CreateView`,
set two or three attributes and you're done. And for managing data internally it ships something
unique among frameworks: the **admin**, a complete back office generated from your models.

## From function to class

```python
# Function view
def book_list(request):
    books = Book.objects.order_by("title")
    return render(request, "books/list.html", {"books": books})

# The same view, generic
from django.views.generic import ListView

class BookList(ListView):
    model = Book
    ordering = ["title"]
    template_name = "books/list.html"
    context_object_name = "books"
```

```python
urlpatterns = [path("books/", BookList.as_view(), name="list")]
```

`as_view()` turns the class into a view function. Each request creates a new instance:
no shared state.

## The main generic views

| Class          | What for                        | Key attributes                                |
|----------------|---------------------------------|-----------------------------------------------|
| `ListView`     | list (with pagination)          | `model`, `queryset`, `ordering`, `paginate_by` |
| `DetailView`   | one object by `pk` or `slug`    | `model`, `context_object_name`                |
| `CreateView`   | create form                     | `model`, `fields`, `success_url`              |
| `UpdateView`   | edit form                       | same                                          |
| `DeleteView`   | confirmation and deletion       | `success_url`                                 |
| `TemplateView` | a static template               | `template_name`                               |
| `RedirectView` | redirect                        | `url` or `pattern_name`                       |

Without `template_name`, Django looks for `<app>/<model>_list.html`, `<app>/<model>_detail.html` or
`<app>/<model>_form.html`.

### Customizing: overriding methods

CBVs are built from methods you can override:

```python
class BookList(ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        if q := self.request.GET.get("q"):
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "")
        return context
```

- `get_queryset()` decides **which objects** are shown: filters, search or only the user's own.
- `get_context_data()` adds variables to the template.
- `self.request`, `self.kwargs` (the URL parameters) and `self.object` are available.
- With `paginate_by`, the template receives `page_obj` and `paginator`, and the page is chosen with
  `?page=2`.

### Creating with validation included

```python
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class BookCreate(CreateView):
    model = Book
    fields = ["title", "author", "year"]          # builds a ModelForm for you
    template_name = "books/form.html"
    success_url = reverse_lazy("list")            # where to redirect after saving
```

GET shows the form; POST validates, saves and redirects (PRG); and if it's invalid, it shows the
form again with errors. That's the whole pattern from the previous chapter in five lines.
`reverse_lazy` instead of `reverse`, because when the class is defined the URLs aren't loaded
yet.

For cross-cutting behavior there are **mixins**: `LoginRequiredMixin` (next chapter),
`PermissionRequiredMixin` and your own.

### Functions or classes?

CBVs shine in standard CRUD. For very specific logic, a function view is usually clearer: you
don't need to know which methods to override. Both are idiomatic.

## The admin

```python
from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "year"]       # list columns
    search_fields = ["title", "author"]               # search box
    list_filter = ["year"]                            # side filters
    ordering = ["title"]
    list_per_page = 50
```

```bash
uv run python manage.py createsuperuser
# → http://127.0.0.1:8000/admin/
```

With that you get listing, search, filters, create, edit, delete, history and per-user
permissions, without writing a single template. You can customize it much further:
`readonly_fields`, `inlines` to edit related objects on the same screen, bulk actions with
`actions`, etc.

The admin is meant for the **internal team**, not for your product's end users.

## In other frameworks

- **Flask**: there are no equivalent CBVs (there's `MethodView`), and you get an admin with
  Flask-Admin.
- **FastAPI**: routers and dependencies play that role for APIs; for a panel, libraries
  like SQLAdmin.

None of them ships anything as complete as the Django admin, and it's one of the strongest
reasons to choose it.

## Summary

- `ListView`, `DetailView`, `CreateView`, `UpdateView` and `DeleteView` + `as_view()`.
- You set attributes (`model`, `fields`, `template_name`, `paginate_by`, `success_url`) and
  override `get_queryset`/`get_context_data` to customize.
- `reverse_lazy` in class attributes.
- `@admin.register(Model)` + `ModelAdmin` (`list_display`, `search_fields`, `list_filter`) gives you a
  complete back office.

## Exercise

A books CRUD with generic views: a list with search and pagination, a detail, a create with
redirect and the admin registration. The templates are in `templates/books/`.

**Further reading:** [Class-based views](https://docs.djangoproject.com/en/stable/topics/class-based-views/),
[Generic display views](https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/),
[The Django admin site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/),
[Classy CBV](https://ccbv.co.uk/) (a reference of every method).
