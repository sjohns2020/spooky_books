from rest_framework import generics, status
from catalogue.models import Book, Author, BookLoan
from .permissions import IsCustomer, IsDeveloper, IsLibrarian
from .serializers import BookSerializer, AuthorSerializer, BookLoanSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


# api/books/ Route - View All and Create
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter  # This custom filter class is in filter.py

    # Only librarians can create
    def get_permissions(self):
        # Instantiates and returns the list of permissions that this view requires.
        if self.request.method == "POST":
            self.permission_classes = [IsLibrarian]
        return super(BookList, self).get_permissions()


# api/books/<int:pk> Route - View One, Update, Delete
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]  # All authenticated users can view
    serializer_class = BookSerializer

    # Only librarians can update and delete
    def get_permissions(self):
        # Instantiates and returns the list of permissions that this view requires.
        if self.request.method == "POST":
            self.permission_classes = [IsLibrarian]
        return super(BookDetail, self).get_permissions()


# api/authors/ Route - View All and Create
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer

    # Only librarians can create
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsLibrarian]
        return super(AuthorList, self).get_permissions()


# api/authors/<int:pk> Route - View One, Update, Delete
class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializer

    # Only librarians can update and delete
    def get_permissions(self):
        # Instantiates and returns the list of permissions that this view requires.
        if self.request.method == "POST":
            self.permission_classes = [IsLibrarian]
        return super(AuthorDetail, self).get_permissions()


# api/bookloans/ Route - View All and Create
class BookLoanList(generics.ListCreateAPIView):
    queryset = BookLoan.objects.all()
    # Only Librarians users can view
    permission_classes = [IsAuthenticated, IsLibrarian]
    serializer_class = BookLoanSerializer


# api/bookloans/<int:pk> Route - View One, Update, Delete
class BookLoanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookLoan.objects.all()
    # Only Librarians users can view
    permission_classes = [IsAuthenticated, IsLibrarian]
    serializer_class = BookLoanSerializer


# api/books/<int:pk>/checkout/ - Customer can checkout a book
class CheckoutBook(APIView):
    # Only Customers chan checkout
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, pk, format=None):
        book = get_object_or_404(Book, pk=pk)
        user = request.user

        if book.is_checked_out():
            return Response(
                {"error": "This book is already checked out."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        loan = book.checkout(user)
        return Response(
            {"message": "Book checked out successfully.", "loan_id": loan.id},
            status=status.HTTP_201_CREATED,
        )


# api/books/<int:pk>/return/ - Customer can return a book
class ReturnBook(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, pk, format=None):
        book = get_object_or_404(Book, pk=pk)
        book_loan = get_object_or_404(
            BookLoan, book=book, user=request.user, returned=False
        )

        book_loan.return_book()
        return Response(
            {"message": "Book returned successfully."}, status=status.HTTP_200_OK
        )
