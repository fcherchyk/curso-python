from django.contrib import admin
from django.db import models
from django.urls import path, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    class Meta:
        app_label = "library"

    def __str__(self) -> str:
        return self.title


class BookList(ListView):
    model = Book
    ordering = ["title"]
    paginate_by = 3
    template_name = "books/list.html"
    context_object_name = "books"

    def get_queryset(self):  # type: ignore[no-untyped-def]
        qs = super().get_queryset()
        if q := self.request.GET.get("q"):
            qs = qs.filter(title__icontains=q)
        return qs


class BookDetail(DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"


class BookCreate(CreateView):
    model = Book
    fields = ["title", "author", "year"]
    template_name = "books/form.html"
    success_url = reverse_lazy("list")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "year"]
    search_fields = ["title", "author"]
    list_filter = ["year"]


urlpatterns = [
    path("books/", BookList.as_view(), name="list"),
    path("books/<int:pk>/", BookDetail.as_view(), name="detail"),
    path("books/new/", BookCreate.as_view(), name="create"),
]
