from . import views
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from drf_yasg import openapi

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
    path("books/", views.BookList.as_view(), name="api_books_list"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="api_books_detail"),
    path("authors/", views.AuthorList.as_view(), name="api_authors_list"),
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name="api_authors_detail"),
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
