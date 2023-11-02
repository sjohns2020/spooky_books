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
        permissions = [
            # For customer group
            ("customers_can_view_books", "Can view books"),
            ("customers_can_view_authors", "Can view authors"),
            ("customers_can_checkout_book", "Can checkout book"),
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
