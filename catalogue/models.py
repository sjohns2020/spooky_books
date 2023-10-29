from django.db import models

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    publication_year = models.IntegerField()
    ISBN = models.CharField(max_length=20, unique=True)
    image = models.CharField(
        max_length=255,
        default="https://upload.wikimedia.org/wikipedia/commons/3/3f/Placeholder_view_vector.svg",
    )

    def __str__(self):
        return self.title
