# serializers.py
from rest_framework import serializers
from catalogue.models import Author, Book, BookLoan


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "publication_year", "ISBN", "image"]


class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = ["id", "user", "book", "checkout_date", "due_date", "returned"]
