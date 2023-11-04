from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

# from django.contrib.auth.models import Permission


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    # Book has One-to-Many relationship with an Author
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

    def save(self, *args, **kwargs):
        if not self.image:
            # When a book is saved, If image is None, assign the default value
            self.image = "https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg"
        super().save(*args, **kwargs)

    def checkout(self, user):
        if self.is_checked_out():
            raise ValueError("This book is already checked out.")
        # Calculate the due_date as 30 days from now
        due_date = timezone.now().date() + timedelta(days=30)
        loan = BookLoan.objects.create(user=user, book=self, due_date=due_date)
        return loan

    def is_checked_out(self):
        # Looks through all the books bookloans and checks if
        # any of them have not been returned.
        return self.bookloan_set.filter(returned=False).exists()


class BookLoan(models.Model):
    # Book has Many-to-Many relationship with an User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def is_overdue(self):
        # Returns True if the book is overdue
        return timezone.now().date() > self.due_date and not self.returned

    def return_book(self):
        self.returned = True
        self.save()

    @classmethod
    def get_all_current_loans(cls):
        # This is a method that operates on all current loans,
        # we use cls to access the model manager (objects) and
        # perform a query that applies to the class as a whole,
        # rather than an individual instance.
        return cls.objects.filter(returned=False)

    @classmethod
    def get_all_overdue_loans(cls):
        today = timezone.now().date()
        # Filter for loans that are past due and not yet returned
        return cls.objects.filter(Q(due_date__lt=today) & Q(returned=False))
