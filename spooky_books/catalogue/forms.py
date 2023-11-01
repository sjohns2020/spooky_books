# forms.py
from django import forms
from .models import Book


class NewForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]


class EditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "ISBN", "image"]
