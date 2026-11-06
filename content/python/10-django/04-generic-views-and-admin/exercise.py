"""Class-based views and the admin.

The Book model is already here. Write:

1. BookList (ListView): template "books/list.html", variable `books`, ordered by title,
   paginate_by=3 and, if ?q=text is present, filter by title (icontains).
2. BookDetail (DetailView): template "books/detail.html", variable `book`.
3. BookCreate (CreateView): fields title, author and year; template "books/form.html";
   after saving it redirects to the list (reverse_lazy).
4. URLs: "books/" name="list", "books/<int:pk>/" name="detail", "books/new/" name="create".
5. Admin: register Book with list_display = ["title", "author", "year"],
   search_fields = ["title", "author"] and list_filter = ["year"].
"""

from django.contrib import admin  # noqa: F401
from django.db import models
from django.urls import path, reverse_lazy  # noqa: F401
from django.views.generic import CreateView, DetailView, ListView  # noqa: F401


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    class Meta:
        app_label = "library"

    def __str__(self) -> str:
        return self.title


urlpatterns: list = []
