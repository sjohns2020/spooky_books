from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from catalogue.models import Book, Author

# Create your tests here.


class BookTests(APITestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.author1 = Author.objects.create(
            first_name="Mary", last_name="Wollstonecraft Shelley"
        )
        self.author2 = Author.objects.create(first_name="Darren", last_name="Shan")
        Book.objects.create(
            title="Frankenstein",
            author=self.author1,
            publication_year=1994,
            ISBN="9781561563098",
            image="http://books.google.com/books/content?id=4dHXkNcpIXgC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )
        Book.objects.create(
            title="Lord of the Shadows",
            author=self.author2,
            publication_year=2004,
            ISBN="9780007159208",
            image="http://books.google.com/books/content?id=Q3fusSYGLuwC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )
        Book.objects.create(
            title="Slawter",
            author=self.author2,
            publication_year=2007,
            ISBN="9780007231386",
            image="http://books.google.com/books/content?id=zRCISxY0oDwC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )
        self.book1 = Book.objects.get(title="Frankenstein")
        self.book2 = Book.objects.get(title="Lord of the Shadows")
        self.book3 = Book.objects.get(title="Slawter")

        # URL for the books list
        self.books_list_url = reverse("api_books_list")
        # URL for the authors list
        self.authors_list_url = reverse("api_authors_list")

    def test_get_books_list(self):
        response = self.client.get(self.books_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_authors_list(self):
        response = self.client.get(self.authors_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_books_detail(self):
        url = reverse("api_books_detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Frankenstein")

    def test_get_authors_detail(self):
        url = reverse("api_authors_detail", kwargs={"pk": self.author1.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Mary")

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": self.author1.pk,
            "publication_year": 2022,
            "ISBN": "1234567890123",
            "image": "http://example.com/image.jpg",
        }
        response = self.client.post(self.books_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_create_author(self):
        data = {
            "first_name": "New",
            "last_name": "Author",
        }
        response = self.client.post(self.authors_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], "New")

    def test_update_book(self):
        data = {
            "title": "Updated Book",
        }
        url = reverse("api_books_detail", kwargs={"pk": self.book1.pk})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    def test_update_author(self):
        data = {
            "first_name": "Updated FirstName",
        }
        url = reverse("api_authors_detail", kwargs={"pk": self.author1.pk})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated FirstName")

    def test_delete_book(self):
        url = reverse("api_books_detail", kwargs={"pk": self.book1.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_author(self):
        url = reverse("api_authors_detail", kwargs={"pk": self.author1.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_books_by_title(self):
        response = self.client.get(
            self.books_list_url, {"title": "frank"}, format="json"
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Frankenstein")

    def test_filter_books_by_isbn(self):
        response = self.client.get(self.books_list_url, {"ISBN": "9780"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["ISBN"], "9780007159208")

    def test_filter_books_by_authors_first_name(self):
        response = self.client.get(
            self.books_list_url, {"author_name": "Darren"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            book_instance = Book.objects.get(id=book["id"])
            self.assertEqual(book_instance.author.first_name, "Darren")

    def test_filter_books_by_authors_last_name(self):
        response = self.client.get(
            self.books_list_url, {"author_name": "Shan"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            book_instance = Book.objects.get(id=book["id"])
            self.assertEqual(book_instance.author.last_name, "Shan")
