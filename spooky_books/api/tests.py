from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from catalogue.models import Book, Author
from django.contrib.auth.models import User, Group

# Create your tests here.


# Tests for DRF API routes.
class BookTests(APITestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.author1 = Author.objects.create(
            first_name="Mary", last_name="Wollstonecraft Shelley"
        )
        self.author2 = Author.objects.create(first_name="Darren", last_name="Shan")
        self.author3 = Author.objects.create(first_name="Stephen", last_name="King")
        self.book1 = Book.objects.create(
            title="Frankenstein",
            author=self.author1,
            publication_year=1994,
            ISBN="9781561563098",
            image="http://books.google.com/books/content?id=4dHXkNcpIXgC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )
        self.book2 = Book.objects.create(
            title="Lord of the Shadows",
            author=self.author2,
            publication_year=2004,
            ISBN="9780007159208",
            image="http://books.google.com/books/content?id=Q3fusSYGLuwC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )
        self.book3 = Book.objects.create(
            title="Slawter",
            author=self.author2,
            publication_year=2007,
            ISBN="9780007231386",
            image="http://books.google.com/books/content?id=zRCISxY0oDwC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )

        # Create a user and a "Librarian" group.
        self.librarian_user = User.objects.create_user(
            "librarian", "librarian@example.com", "password"
        )
        librarian_group = Group.objects.create(name="Librarian")
        self.librarian_user.groups.add(librarian_group)
        self.librarian_user.save()

        # Create a user and a "Customer" group.
        self.customer_user = User.objects.create_user(
            "customer", "customer@example.com", "password"
        )
        customer_group = Group.objects.create(name="Customer")
        self.customer_user.groups.add(customer_group)
        self.customer_user.save()

        # Create a user and a "Developer" group.
        self.developer_user = User.objects.create_user(
            "developer", "developer@example.com", "password"
        )
        developer_group = Group.objects.create(name="Developer")
        self.developer_user.groups.add(developer_group)
        self.developer_user.save()

    # Books INDEX View
    def test_get_books_list__by_customer(self):
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("api_books_list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_books_list__by_librarian(self):
        self.client.login(username="librarian", password="password")
        response = self.client.get(reverse("api_books_list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_books_list__by_developer(self):
        self.client.login(username="developer", password="password")
        response = self.client.get(reverse("api_books_list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # Author Index View
    def test_get_authors_list__by_customer(self):
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("api_authors_list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_authors_list__by_librarian(self):
        self.client.login(username="librarian", password="password")
        response = self.client.get(reverse("api_authors_list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_authors_list__by_developer(self):
        self.client.login(username="developer", password="password")
        response = self.client.get(reverse("api_authors_list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # Books Show View
    def test_get_books_detail__by_customer(self):
        self.client.login(username="customer", password="password")
        book = Book.objects.get(title=self.book1.title)
        url = reverse("api_books_detail", kwargs={"pk": book.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Frankenstein")

    def test_get_books_detail__by_librarian(self):
        self.client.login(username="librarian", password="password")
        book = Book.objects.get(title=self.book1.title)
        url = reverse("api_books_detail", kwargs={"pk": book.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Frankenstein")

    def test_get_books_detail__by_developer(self):
        self.client.login(username="developer", password="password")
        book = Book.objects.get(title=self.book1.title)
        url = reverse("api_books_detail", kwargs={"pk": book.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Frankenstein")

    # Author Show View
    def test_get_authors_detail__by_customer(self):
        self.client.login(username="customer", password="password")
        author = Author.objects.get(first_name=self.author1.first_name)
        url = reverse("api_authors_detail", kwargs={"pk": author.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Mary")

    def test_get_authors_detail__by_librarian(self):
        self.client.login(username="librarian", password="password")
        author = Author.objects.get(first_name=self.author1.first_name)
        url = reverse("api_authors_detail", kwargs={"pk": author.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Mary")

    def test_get_authors_detail__by_developer(self):
        self.client.login(username="developer", password="password")
        author = Author.objects.get(first_name=self.author1.first_name)
        url = reverse("api_authors_detail", kwargs={"pk": author.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Mary")

    # Book Create View
    # def test_create_book__by_librarian(self):
    #     self.client.login(username="librarian", password="password")
    #     author_id = Author.objects.get(first_name="Stephen").id
    #     data = {
    #         "title": "New Book",
    #         "author": str(author_id),
    #         "publication_year": "2022",
    #         "ISBN": "1234567890123",
    #         "image": "http://example.com/image.jpg",
    #     }
    #     response = self.client.post(reverse("api_books_list"), data, format="json")
    #     print("Response data:", response.data)  # This will show you the response data.
    #     print(
    #         "Response status code:", response.status_code
    #     )  # This will show you the status code.
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["title"], "New Book")

    def test_create_book__customer_cannot_create(self):
        self.client.login(username="customer", password="password")
        author_id = Author.objects.get(first_name="Stephen").id
        data = {
            "title": "New Book",
            "author": str(author_id),
            "publication_year": "2022",
            "ISBN": "1234567890123",
            "image": "http://example.com/image.jpg",
        }
        self.client.post(reverse("api_books_list"), data, format="json")
        self.assertFalse(Book.objects.filter(title="New Book").exists())

    def test_create_book____developer_cannot_create(self):
        self.client.login(username="developer", password="password")
        author_id = Author.objects.get(first_name="Stephen").id
        data = {
            "title": "New Book",
            "author": str(author_id),
            "publication_year": "2022",
            "ISBN": "1234567890123",
            "image": "http://example.com/image.jpg",
        }
        self.client.post(reverse("api_books_list"), data, format="json")
        self.assertFalse(Book.objects.filter(title="New Book").exists())

    # Create Author
    # def test_create_author__by_librarian(self):
    #     self.client.login(username="librarian", password="password")
    #     data = {"first_name": "New", "last_name": "Author"}
    #     response = self.client.post(reverse("api_authors_list"), data, format="json")
    #     print("Response data:", response.data)  # This will show you the response data.
    #     print(
    #         "Response status code:", response.status_code
    #     )  # This will show you the status code.

    #     # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["first_name"], "New")

    def test_create_author__customer_cannot_create(self):
        self.client.login(username="customer", password="password")
        data = {"first_name": "New", "last_name": "Author"}
        response = self.client.post(reverse("api_authors_list"), data, format="json")
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(Author.objects.filter(first_name="New").exists())

    def test_create_author__developer_cannot_create(self):
        self.client.login(username="developer", password="password")
        data = {"first_name": "New", "last_name": "Author"}
        response = self.client.post(reverse("api_authors_list"), data, format="json")
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(Author.objects.filter(first_name="New").exists())

    def test_update_book__by_librarian(self):
        self.client.login(username="librarian", password="password")
        book_to_edit = Book.objects.get(title=self.book2.title)
        data = {"title": "Updated Book"}
        url = reverse("api_books_detail", kwargs={"pk": book_to_edit.id})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_book = Book.objects.get(title="Updated Book")
        self.assertEqual(updated_book.title, "Updated Book")

    def test_update_author__by_librarian(self):
        self.client.login(username="librarian", password="password")
        author_to_edit = Author.objects.get(first_name=self.author1.first_name)

        data = {"first_name": "Updated FirstName"}
        url = reverse("api_authors_detail", kwargs={"pk": author_to_edit.id})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_author = Author.objects.get(first_name="Updated FirstName")
        self.assertEqual(updated_author.first_name, "Updated FirstName")

    def test_delete_book__by_librarian(self):
        self.client.login(username="librarian", password="password")
        book_to_delete = Book.objects.get(title="Frankenstein")
        self.assertTrue(Book.objects.filter(title="Frankenstein").exists())
        url = reverse("api_books_detail", kwargs={"pk": book_to_delete.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_author__by_librarian(self):
        self.client.login(username="librarian", password="password")
        author_to_delete = Author.objects.get(first_name=self.author1.first_name)
        self.assertTrue(
            Author.objects.filter(first_name=self.author1.first_name).exists()
        )
        url = reverse("api_authors_detail", kwargs={"pk": author_to_delete.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_books_by_title__by_librarian(self):
        self.client.login(username="librarian", password="password")
        response = self.client.get(
            reverse("api_books_list"), {"title": "frank"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Frankenstein")

    def test_filter_books_by_title__by_customer(self):
        self.client.login(username="customer", password="password")
        response = self.client.get(
            reverse("api_books_list"), {"title": "frank"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Frankenstein")

    def test_filter_books_by_title__by_developer(self):
        self.client.login(username="developer", password="password")
        response = self.client.get(
            reverse("api_books_list"), {"title": "frank"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Frankenstein")

    def test_filter_books_by_isbn__by_librarian(self):
        self.client.login(username="librarian", password="password")
        response = self.client.get(
            reverse("api_books_list"), {"ISBN": "9780"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["ISBN"], "9780007159208")

    def test_filter_books_by_authors_first_name__by_librarian(self):
        self.client.login(username="librarian", password="password")
        response = self.client.get(
            reverse("api_books_list"), {"author_name": "Darren"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            book_instance = Book.objects.get(id=book["id"])
            self.assertEqual(book_instance.author.first_name, "Darren")

    def test_filter_books_by_authors_last_name__by_librarian(self):
        self.client.login(username="librarian", password="password")
        response = self.client.get(
            reverse("api_books_list"), {"author_name": "Shan"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            book_instance = Book.objects.get(id=book["id"])
            self.assertEqual(book_instance.author.last_name, "Shan")
