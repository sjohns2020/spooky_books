from django.db import models
from django.contrib.auth.models import User

# from django.utils import timezone
# Create your models here.


# User Profile Class with One to One Relationship with a User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username

    _is_librarian = None
    _is_customer = None
    _is_developer = None

    @property
    def is_librarian(self):
        if self._is_librarian is None:
            self._is_librarian = self.user.groups.filter(name="Librarian").exists()
        return self._is_librarian

    @property
    def is_customer(self):
        if self._is_customer is None:
            self._is_customer = self.user.groups.filter(name="Customer").exists()
        return self._is_customer

    @property
    def is_developer(self):
        if self._is_developer is None:
            self._is_developer = self.user.groups.filter(name="Developer").exists()
        return self._is_developer
