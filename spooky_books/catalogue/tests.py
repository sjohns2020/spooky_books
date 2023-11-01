from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Book

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
        Book.objects.create(
            title="Frankenstein",
            author=self.author,
            publication_year=1994,
            ISBN="9781561563098",
            image="http://books.google.com/books/content?id=4dHXkNcpIXgC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )
        self.book1 = Book.objects.get(title="Frankenstein")

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


# View Functions Tests
class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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

    # INDEX-View Test
    def test_index_view(self):
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    # SEARCH Tests
    def test_search_by_title(self):
        # This test checks if the view can handle and correctly filter by title
        response = self.client.get(reverse("books_list"), {"title": "Frankenstein"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    def test_search_by_authors__first_name(self):
        # This test checks if the view can handle and correctly filter by author
        response = self.client.get(reverse("books_list"), {"author": "Darren"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Slawter")
        self.assertContains(response, "Lord of the Shadows")

    def test_search_by_author__last_name(self):
        # This test checks if the view can handle and correctly filter by author
        response = self.client.get(reverse("books_list"), {"author": "Shan"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Slawter")
        self.assertContains(response, "Lord of the Shadows")

    def test_search_by_ISBN(self):
        # This test checks if the view can handle and correctly filter by ISBN
        response = self.client.get(reverse("books_list"), {"ISBN": "9780007231386"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Slawter")

    def test_search_by_all_criteria(self):
        # This test checks if the view can handle and correctly filter by all query parameters together
        response = self.client.get(
            reverse("books_list"),
            {"title": "Frankenstein", "author": "Shelley", "ISBN": "1234567890"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    # SHOW-View Test
    def test_new_view(self):
        response = self.client.get(reverse("books_show", args=(self.book1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    # NEW-View Test
    def test_new_view(self):
        response = self.client.get(reverse("books_new"))
        self.assertEqual(response.status_code, 200)

    # EDIT-View Test
    def test_new_view(self):
        response = self.client.get(reverse("books_edit", args=(self.book2.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lord of the Shadows")

    # DELETE-View Test
    def test_delete_view(self):
        # Ensure the book exists before deletion
        self.assertTrue(Book.objects.filter(id=self.book3.id).exists())

        # Simulate a deletion request.
        response = self.client.post(reverse("books_delete", args=(self.book3.id,)))

        # Check that the delete view redirects redirect (redirects are status code 302)
        self.assertEqual(response.status_code, 302)

        # Ensure the book no longer exists in the database
        self.assertFalse(Book.objects.filter(id=self.book3.id).exists())
