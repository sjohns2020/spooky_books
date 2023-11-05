from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from accounts.models import UserProfile
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm


# Create your views here.


# Register new user Form
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            UserProfile.objects.create(user=user)  # Create a UserProfile for the user

            # Determine the user's group based on your criteria
            selected_role = request.POST.get("role")
            group = None
            if selected_role == "customer":
                group = Group.objects.get(name="Customer")
            elif selected_role == "librarian":
                group = Group.objects.get(name="Librarian")
                user.is_staff = True
            elif selected_role == "developer":
                group = Group.objects.get(name="Developer")
                user.is_staff = True

            if group:
                user.groups.add(group)  # Assign the user to the group
                user.save()  # Save the user with updated is_staff status

            # Authenticate and login the user
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
            return redirect("books_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
