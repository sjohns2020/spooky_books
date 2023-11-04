from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Book, BookLoan
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.models import User, Group


# Create your tests here.


# Author Tests
class AuthorModelTest(TestCase):
    def setUp(self):
        Author.objects.create(first_name="Sean", last_name="Johnson")
        # Couldn't grab object by ID because it changes for every test
        self.author1 = Author.objects.get(first_name="Sean", last_name="Johnson")

    def test_author_has__first_name(self):
        actual = self.author1.first_name
        expected = "Sean"
        self.assertEqual(actual, expected)

    def test_author_has__last_name(self):
        actual = self.author1.last_name
        expected = "Johnson"
        self.assertEqual(actual, expected)


# Book Tests
class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Mary", last_name="Wollstonecraft Shelley"
        )
        self.book1 = Book.objects.create(
            title="Frankenstein",
            author=self.author,
            publication_year=1994,
            ISBN="9781561563098",
            image="http://books.google.com/books/content?id=4dHXkNcpIXgC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )

    def test_book_has__a_title(self):
        actual = self.book1.title
        expected = "Frankenstein"
        self.assertEqual(actual, expected)

    def test_book_has__an_author(self):
        actual = self.book1.author.first_name
        expected = "Mary"
        self.assertEqual(actual, expected)

    def test_book_has__a_publication_year(self):
        actual = self.book1.publication_year
        expected = 1994
        self.assertEqual(actual, expected)

    def test_book_has__an_ISBN(self):
        actual = self.book1.ISBN
        expected = "9781561563098"
        self.assertEqual(actual, expected)

    def test_book_has__an_image(self):
        actual = self.book1.image
        expected = "http://books.google.com/books/content?id=4dHXkNcpIXgC&printsec=frontcover&img=1&zoom=1&source=gbs_api"
        self.assertEqual(actual, expected)


# BookLoans Tests
class BookLoanModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Mary", last_name="Wollstonecraft Shelley"
        )
        self.book = Book.objects.create(
            title="Frankenstein",
            author=self.author,
            publication_year=1994,
            ISBN="9781561563098",
            image="http://books.google.com/books/content?id=4dHXkNcpIXgC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )
        self.user = User.objects.create_user(
            "sean_jo", "sean_jo@example.com", "sean12345"
        )

        self.loan = BookLoan.objects.create(
            user=self.user, book=self.book, due_date=date.today(), returned=False
        )

    def test_BookLoan_has_a_user(self):
        actual = self.loan.user.username
        expected = "sean_jo"
        self.assertEqual(actual, expected)

    def test_BookLoan_has_an_book(self):
        actual = self.loan.book.title
        expected = "Frankenstein"
        self.assertEqual(actual, expected)

    def test_BookLoan_has_a_checkout_date(self):
        actual = self.loan.checkout_date
        expected = date.today()
        self.assertEqual(actual, expected)

    def test_BookLoan_has_a_due_date(self):
        actual = self.loan.due_date
        expected = date.today()
        self.assertEqual(actual, expected)

    def test_BookLoan_has_a_returned_property(self):
        actual = self.loan.returned
        expected = False
        self.assertEqual(actual, expected)
