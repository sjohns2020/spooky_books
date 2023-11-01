# forms.py
from django import forms
from .models import Book


# Only want the user to enter title and select author
# The New View will add the isbn, image, year from Google API
class NewForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]


class EditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "ISBN", "image"]
