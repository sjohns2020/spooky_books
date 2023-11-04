from django.urls import path
from . import views

# Internal Full Stack Django Routes
urlpatterns = [
    # INDEX
    path("", views.index, name="books_list"),
    # SHOW
    path("<int:id>/", views.show, name="books_show"),
    # NEW
    path("new/", views.new, name="books_new"),
    # EDIT
    path("<int:id>/edit/", views.edit, name="books_edit"),
    # DELETE
    path("<int:id>/delete/", views.delete, name="books_delete"),
    # Checkout Book
    path("<int:id>/checkout/", views.checkout_book, name="books_checkout"),
    # Return Book
    path("<int:id>/return/", views.return_book, name="books_return"),
    # Return Book
    path("loans/", views.loans, name="books_loans"),
]
