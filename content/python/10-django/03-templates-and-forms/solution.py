from django import forms
from django.shortcuts import redirect, render
from django.urls import path

MESSAGES: list[dict[str, str]] = []


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, min_length=10)

    def clean_name(self) -> str:
        return self.cleaned_data["name"].strip().title()

    def clean(self):  # type: ignore[no-untyped-def]
        data = super().clean()
        if "spam" in data.get("message", "").lower():
            raise forms.ValidationError("The message looks like spam")
        return data


def contact(request):  # type: ignore[no-untyped-def]
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            MESSAGES.append(form.cleaned_data)
            return redirect("thanks")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


def thanks(request):  # type: ignore[no-untyped-def]
    last = MESSAGES[-1]["name"] if MESSAGES else None
    return render(request, "thanks.html", {"name": last, "total": len(MESSAGES)})


urlpatterns = [
    path("contact/", contact, name="contact"),
    path("thanks/", thanks, name="thanks"),
]
