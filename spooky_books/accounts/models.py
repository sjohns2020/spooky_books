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

    def is_librarian(self):
        return self.groups.filter(name="Librarian").exists()

    def is_customer(self):
        return self.groups.filter(name="Customer").exists()

    def is_developer(self):
        return self.groups.filter(name="Developer").exists()
