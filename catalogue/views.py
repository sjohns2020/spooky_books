from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book
from .forms import BookForm

# Create your views here.


def index(request):
    books = Book.objects.all()
    return render(request, "books/index.html", {"books": books})


def details(request, id):
    # if type(id) == int
    book = get_object_or_404(Book, pk=id)
    return render(request, "books/show.html", {"book": book})


def new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books_list")
    else:
        form = BookForm()
    return render(request, "books/new.html", {"form": form})


def edit(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books_show", id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, "books/edit.html", {"form": form, "book": book})


def delete(request, id):
    book = get_object_or_404(Book, pk=id)
    book.delete()
    return redirect("books_list")
