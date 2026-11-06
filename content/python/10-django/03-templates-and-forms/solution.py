from django import forms
from django.shortcuts import redirect, render
from django.urls import path

MENSAJES: list[dict[str, str]] = []


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea, min_length=10)

    def clean_nombre(self) -> str:
        return self.cleaned_data["nombre"].strip().title()

    def clean(self):  # type: ignore[no-untyped-def]
        datos = super().clean()
        if "spam" in datos.get("mensaje", "").lower():
            raise forms.ValidationError("El mensaje parece spam")
        return datos


def contacto(request):  # type: ignore[no-untyped-def]
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            MENSAJES.append(form.cleaned_data)
            return redirect("gracias")
    else:
        form = ContactoForm()
    return render(request, "contacto.html", {"form": form})


def gracias(request):  # type: ignore[no-untyped-def]
    ultimo = MENSAJES[-1]["nombre"] if MENSAJES else None
    return render(request, "gracias.html", {"nombre": ultimo, "total": len(MENSAJES)})


urlpatterns = [
    path("contacto/", contacto, name="contacto"),
    path("gracias/", gracias, name="gracias"),
]
