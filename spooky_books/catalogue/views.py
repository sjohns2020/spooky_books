from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from .models import *
from .forms import *
from .utils import *
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


# Create your views here.


def is_librarian(user):
    return user.groups.filter(name__in=["Librarian"]).exists()


def is_customer(user):
    return user.groups.filter(name__in=["Customer"]).exists()


def is_developer(user):
    return user.groups.filter(name__in=["Developer"]).exists()


# INDEX
@login_required
def index(request):
    # Handle Filter queries for title, author and ISBN
    title_query = request.GET.get("title", "")
    author_query = request.GET.get("author", "")
    isbn_query = request.GET.get("ISBN", "")

    # Get all Books
    books = Book.objects.all()

    # If a title query is provided, filter books by title
    if title_query:
        books = books.filter(title__icontains=title_query)

    # If an author query is provided, filter books by author's first or last name
    # Allows user to query authors full name
    if author_query:
        books = books.filter(
            # Q is a class that represents a query expression
            # used to perform complex database lookups and
            # filter operations. It allows you to build more
            # complex queries by combining multiple conditions
            # using logical operators like AND, OR, and NOT.
            Q(author__first_name__icontains=author_query)
            | Q(author__last_name__icontains=author_query)
        )

    # If an ISBN query is provided, filter books by ISBN
    if isbn_query:
        books = books.filter(ISBN__icontains=isbn_query)
    return render(request, "books/index.html", {"books": books})


# SHOW
@login_required
def show(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, "books/show.html", {"book": book})


# New form only requires a Title and Author Name
@login_required
@user_passes_test(is_librarian)
def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            author_id = author.id  # Get the author's ID
            # Use utils methods to fetch year, isbn and image from Google Books API
            publication_year = get_publication_year(title, author)
            isbn = get_isbn(title, author)
            image = get_thumbnail_image(title, author)

            # Create a new Book instance
            book = Book(
                title=title,
                author_id=author_id,
                publication_year=publication_year,
                ISBN=isbn,
                image=image,
            )
            book.save()
            return redirect("books_list")
    else:
        form = NewForm()

    return render(request, "books/new.html", {"form": form})


# EDIT
@login_required
@user_passes_test(is_librarian)
def edit(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        form = EditForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books_show", id=book.id)
    else:
        form = EditForm(instance=book)
    return render(request, "books/edit.html", {"form": form, "book": book})


# DELETE
@login_required
@user_passes_test(is_librarian)
def delete(request, id):
    book = get_object_or_404(Book, pk=id)
    book.delete()
    return redirect("/books_list")


# Handler to check if book is available to checkout
def book_available_for_checkout(book, user):
    # Check if the book is already checked out by the user
    if BookLoan.objects.filter(book=book, returned=False).exclude(user=user).exists():
        return False
    if BookLoan.objects.filter(book=book, user=user, due_date__isnull=True).exists():
        return False

    # Check if the book is not overdue for return
    today = timezone.now()
    if BookLoan.objects.filter(book=book, due_date__gt=today).exists():
        return False

    return True


# @login_required
# @user_passes_test(is_customer)
def checkout_book(request, id):
    book = get_object_or_404(Book, pk=id)
    user = request.user

    # Check if the book is available for checkout
    if not book_available_for_checkout(book, user):
        loan = BookLoan.objects.get(book=book, returned=False)
        return render(request, "books/unavailable_book.html", loan=loan)

    # Create a new BookLoan instance
    BookLoan.objects.create(
        user=user, book=book, due_date=timezone.now() + timezone.timedelta(days=14)
    )
    return redirect("books_show", id=book.id)


# @login_required
# @user_passes_test(is_customer)
def return_book(request, id):
    book = get_object_or_404(Book, pk=id)
    user = request.user

    # Create a new BookLoan instance
    BookLoan.objects.update(returned=True)
    return redirect("books_show", id=book.id)
