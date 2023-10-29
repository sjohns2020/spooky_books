from django.urls import path
from . import views

urlpatterns = [
    # Name - optional arguments to let us refer to this route elsewhere in the app.
    path("", views.index, name="books_list"),
    path("details/", views.details, name="books_details"),
    path("new/", views.new, name="books_new"),
    path("edit/", views.edit, name="books_edit"),
]
