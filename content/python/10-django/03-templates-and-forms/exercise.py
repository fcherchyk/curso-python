"""Templates and forms.

1. ContactForm (forms.Form):
   - name: CharField(max_length=50); clean_name → no surrounding spaces and in Title Case
   - email: EmailField()
   - message: CharField(widget=forms.Textarea, min_length=10)
   - clean(): if the message contains "spam" (case-insensitive) →
     ValidationError("The message looks like spam")

2. contact view (URL "contact/", name="contact"):
   - GET → render "contact.html" with an empty form
   - valid POST → MESSAGES.append(form.cleaned_data) and redirect to "thanks"
   - invalid POST → re-render the bound form (status 200)

3. thanks view (URL "thanks/", name="thanks"):
   → render "thanks.html" with name = name from the last message (or None) and total = len(MESSAGES)

The templates are in templates/ (see the lesson).
"""

from django import forms  # noqa: F401
from django.shortcuts import redirect, render  # noqa: F401
from django.urls import path  # noqa: F401

MESSAGES: list[dict[str, str]] = []


class ContactForm(forms.Form):
    pass


urlpatterns: list = []
