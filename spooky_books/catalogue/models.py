from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Publication year and image can be None to help with adding a book
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    publication_year = models.IntegerField(null=True, blank=True)
    ISBN = models.CharField(max_length=20)
    image = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        default="https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
    )

    def __str__(self):
        return self.title

    # If image is None, assign the default value
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg"
        super().save(*args, **kwargs)


class BookLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()  # date for returning the book
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
