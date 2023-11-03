from django.db import models
from django.contrib.auth.models import User

# from django.utils import timezone
# Create your models here.


# User Profile Class with One to One Relationship with a User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # __str__ method determines how UserProfile will display in admin portal
    def __str__(self):
        return self.user.username

    class Meta:
        # There are 3 user Groups with different permissions.
        # Customers -  Can only see books only they can checkout a book
        # Librarians -  Can perform All CRUD on books and Authors and BookLoans
        # Developers -  Can't view BookLoans or check books out but can do everything else

        permissions = [
            # For customer group
            ("customers_could_view_books", "Can view books"),
            ("customers_could_view_authors", "Can view authors"),
            ("customers_could_checkout_book", "Can checkout book"),
            # For librarian group
            ("librarians_can_view_books", "Can view books"),
            ("librarians_can_view_authors", "Can view authors"),
            ("librarians_can_add_books", "Can add books"),
            ("librarians_can_update_books", "Can update books"),
            ("librarians_can_delete_books", "Can delete books"),
            ("librarians_can_add_authors", "Can add authors"),
            ("librarians_can_update_authors", "Can update authors"),
            ("librarians_can_delete_authors", "Can delete authors"),
            ("librarians_can_view_bookloans", "Can view bookloans"),
            ("librarians_can_add_bookloans", "Can add bookloans"),
            ("librarians_can_update_bookloans", "Can update bookloans"),
            ("librarians_can_delete_bookloans", "Can delete bookloans"),
        ]
