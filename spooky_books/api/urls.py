from . import views
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from drf_yasg import openapi

# Required by Swagger to create API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Spooky Books",
        default_version="v1",
        description="Spooky Books Catalogue.  Brows your favorite spooky books and get spooked",
        terms_of_service="https://github.com/sjohns2020/spooky_books",
        contact=openapi.Contact(email="seanjo86@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # API ROUTES
    # api/books/ Route - View All and Create Books
    path("books/", views.BookList.as_view(), name="api_books_list"),
    # api/books/<id> Route - View One, Update, Delete a Book
    path("books/<int:pk>/", views.BookDetail.as_view(), name="api_books_detail"),
    # api/authors/ Route - View All and Create Authors
    path("authors/", views.AuthorList.as_view(), name="api_authors_list"),
    # api/authors/<id> Route - View One, Update, Delete an Author
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name="api_authors_detail"),
    # api/bookloans/ Route - View All and Create BookLoans
    path("bookloans/", views.BookLoanList.as_view(), name="api_bookloans_list"),
    # api/bookloans/<id> Route - View One, Update, Delete a BookLoans
    path(
        "bookloans/<int:pk>/",
        views.BookLoanDetail.as_view(),
        name="api_bookloans_detail",
    ),
    # Customer can checkout a book
    path(
        "books/<int:pk>/checkout/",
        views.CheckoutBook.as_view(),
        name="api_checkout_book",
    ),
    # Customer can Return a book
    path("books/<int:pk>/return/", views.ReturnBook.as_view(), name="api_return_book"),
    # Routes for API Documentation with Swagger
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
