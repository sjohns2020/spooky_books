from django.urls import path
from . import views

urlpatterns = [
    # INTERNAL ROUTES
    path("", views.index, name="books_list"),
    path("<int:id>/", views.show, name="books_show"),
    path("new/", views.new, name="books_new"),
    path("<int:id>/edit/", views.edit, name="books_edit"),
    path("<int:id>/delete/", views.delete, name="books_delete"),
]
