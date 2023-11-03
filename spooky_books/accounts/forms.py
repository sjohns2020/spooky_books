from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Customised Registration form to add permissions group
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("librarian", "Librarian"),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "role")
