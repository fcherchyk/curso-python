"""Plantillas y formularios.

1. ContactoForm (forms.Form):
   - nombre: CharField(max_length=50); clean_nombre → sin espacios alrededor y en Title Case
   - email: EmailField()
   - mensaje: CharField(widget=forms.Textarea, min_length=10)
   - clean(): si el mensaje contiene "spam" (sin importar mayúsculas) →
     ValidationError("El mensaje parece spam")

2. Vista contacto (URL "contacto/", name="contacto"):
   - GET → render "contacto.html" con un form vacío
   - POST válido → MENSAJES.append(form.cleaned_data) y redirect a "gracias"
   - POST inválido → re-render del form ligado (status 200)

3. Vista gracias (URL "gracias/", name="gracias"):
   → render "gracias.html" con nombre = nombre del último mensaje (o None) y total = len(MENSAJES)

Las plantillas están en templates/ (ver la lección).
"""

from django import forms  # noqa: F401
from django.shortcuts import redirect, render  # noqa: F401
from django.urls import path  # noqa: F401

MENSAJES: list[dict[str, str]] = []


class ContactoForm(forms.Form):
    pass


urlpatterns: list = []
