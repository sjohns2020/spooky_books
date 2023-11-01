from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm

# Create your views here.


from django.db.models import Q


# INDEX
def index(request):
    title_query = request.GET.get("title", "")
    author_query = request.GET.get("author", "")
    isbn_query = request.GET.get("ISBN", "")

    # Get all Books
    books = Book.objects.all()

    # If a title query is provided, filter books by title
    if title_query:
        books = books.filter(title__icontains=title_query)

    # If an author query is provided, filter books by author's first or last name
    if author_query:
        books = books.filter(
            Q(author__first_name__icontains=author_query)
            | Q(author__last_name__icontains=author_query)
        )

    # If an ISBN query is provided, filter books by ISBN
    if isbn_query:
        books = books.filter(ISBN__icontains=isbn_query)

    return render(request, "books/index.html", {"books": books})


# SHOW
def show(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, "books/show.html", {"book": book})


# NEW
def new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books_list")
    else:
        form = BookForm()
    return render(request, "books/new.html", {"form": form})


# EDIT
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


# DELETE
def delete(request, id):
    book = get_object_or_404(Book, pk=id)
    book.delete()
    return redirect("books_list")
