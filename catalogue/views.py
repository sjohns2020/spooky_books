from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "books/index.html")


def details(request):
    return render(request, "books/show.html")


def new(request):
    return render(request, "books/new.html")


def edit(request):
    return render(request, "books/edit.html")
