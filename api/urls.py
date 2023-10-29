from django.urls import path
from . import views

urlpatterns = [
    # API ROUTES
    path("books/", views.BookList.as_view(), name="api_books_list"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="api_books_detail"),
    path("authors/", views.AuthorList.as_view(), name="api_authors_list"),
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name="api_authors_detail"),
]
