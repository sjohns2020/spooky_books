from rest_framework import generics
from catalogue.models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter


# api/books/ Route - View All and Create
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter  # This custom filter class is in filter.py


# api/books/<id> Route - View One, Update, Delete
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# api/authors/ Route - View All and Create
class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# api/authors/<id> Route - View One, Update, Delete
class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# from django.views.generic import ListView
# class VoteListView(PermissionRequiredMixin, ListView):
#     permission_required = 'can_add_update_delete_books'
#     # Or multiple of permissions
#     permission_required = ('can_add_update_delete_books', 'can_checkout_book')
