from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from accounts.models import UserProfile

# Create your views here.


# Register new user Form
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect("books_list")
    else:
        form = UserCreationForm()

    # This folder must be called registration as Django will look for it
    return render(request, "registration/register.html", {"form": form})
