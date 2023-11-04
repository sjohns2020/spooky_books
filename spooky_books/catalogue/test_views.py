from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Book, BookLoan
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.models import User, Group


# View Functions Tests
class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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

    # DELETE-View Tests
    def test_delete_view__librarian_can_use(self):
        # Log in the librarian user
        self.client.login(username="librarian", password="password")
        # Ensure the book exists before deletion
        self.assertTrue(Book.objects.filter(id=self.book3.id).exists())
        # Simulate a deletion request.
        response = self.client.post(reverse("books_delete", args=(self.book3.id,)))
        # Check that the delete view redirects redirect (redirects are status code 302)
        self.assertEqual(response.status_code, 302)
        # Ensure the book no longer exists in the database
        self.assertFalse(Book.objects.filter(id=self.book3.id).exists())

    def test_delete_view__customer_cannot_use(self):
        # Log in the customer user
        self.client.login(username="customer", password="password")
        # Ensure the book exists before deletion
        self.assertTrue(Book.objects.filter(id=self.book3.id).exists())
        # Try to delete the book as a customer
        response = self.client.post(reverse("books_delete", args=(self.book3.id,)))
        # Ensure the book still exists in the database
        self.assertTrue(Book.objects.filter(id=self.book3.id).exists())

    def test_delete_view__developer_cannot_use(self):
        # Log in the developer user
        self.client.login(username="developer", password="password")
        # Ensure the book exists before deletion
        self.assertTrue(Book.objects.filter(id=self.book3.id).exists())
        # Try to delete the book as a developer
        response = self.client.post(reverse("books_delete", args=(self.book3.id,)))
        # Ensure the book still exists in the database
        self.assertTrue(Book.objects.filter(id=self.book3.id).exists())

    # INDEX-View Test
    def test_index_view__customer_can_view(self):
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    def test_index_view__librarian_can_view(self):
        self.client.login(username="librarian", password="password")
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    def test_index_view__developer_can_view(self):
        self.client.login(username="developer", password="password")
        response = self.client.get(reverse("books_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    # SEARCH Tests
    def test_search_by_title(self):
        # This test checks if the view can handle and correctly filter by title
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("books_list"), {"title": "Frankenstein"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    def test_search_by_authors__first_name(self):
        # This test checks if the view can handle and correctly filter by author
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("books_list"), {"author": "Darren"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Slawter")
        self.assertContains(response, "Lord of the Shadows")

    def test_search_by_author__last_name(self):
        # This test checks if the view can handle and correctly filter by author
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("books_list"), {"author": "Shan"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Slawter")
        self.assertContains(response, "Lord of the Shadows")

    def test_search_by_ISBN(self):
        # This test checks if the view can handle and correctly filter by ISBN
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("books_list"), {"ISBN": "9780007231386"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Slawter")

    def test_search_by_all_criteria(self):
        # This test checks if the view can handle and correctly filter by all query parameters together
        self.client.login(username="customer", password="password")
        response = self.client.get(
            reverse("books_list"),
            {"title": "Frankenstein", "author": "Shelley", "ISBN": "1234567890"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    # SHOW-View Test
    def test_new_view(self):
        self.client.login(username="customer", password="password")
        response = self.client.get(reverse("books_show", args=(self.book1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frankenstein")

    # NEW-View Test
    def test_new_view__librarian_can_create_book(self):
        self.client.login(username="librarian", password="password")
        book_data = {
            "title": "Thinner",
            "author": Author.objects.get(first_name="Stephen").id,
        }
        response = self.client.post(reverse("books_new"), book_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title="Thinner").exists())

    def test_new_view__customer_cannot_create_book(self):
        self.client.login(username="customer", password="password")
        book_data = {
            "title": "Thinner",
            "author": Author.objects.get(first_name="Stephen").id,
        }
        response = self.client.post(reverse("books_new"), book_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(title="Thinner").exists())

    def test_new_view__developer_cannot_create_book(self):
        self.client.login(username="developer", password="password")
        book_data = {
            "title": "Thinner",
            "author": Author.objects.get(first_name="Stephen").id,
        }
        response = self.client.post(reverse("books_new"), book_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(title="Thinner").exists())

    # EDIT-View Test
    def test_edit_view__librarian_can_edit_book(self):
        self.client.login(username="librarian", password="password")
        book_to_edit = Book.objects.get(title=self.book2.title)
        author = Author.objects.get(id=book_to_edit.author.id)
        edit_data = {
            "title": "Updated Book Title",
            "author": author.id,
            "publication_year": 1985,
            "ISBN": "9780007159208",
            "image": "http://books.google.com/books/content?id=1YP-hfna5ewC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        }

        response = self.client.post(
            reverse("books_edit", args=[book_to_edit.id]), edit_data
        )
        self.assertEqual(response.status_code, 302)
        updated_book = Book.objects.get(title="Updated Book Title")
        self.assertEqual(updated_book.title, "Updated Book Title")

    def test_edit_view__customer_cannot_edit_book(self):
        self.client.login(username="customer", password="password")
        book_to_edit = Book.objects.get(title=self.book2.title)
        author = Author.objects.get(id=book_to_edit.author.id)
        edit_data = {
            "title": "Updated Book Title",
            "author": author.id,
            "publication_year": 1985,
            "ISBN": "9780007159208",
            "image": "http://books.google.com/books/content?id=1YP-hfna5ewC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        }

        response = self.client.post(
            reverse("books_edit", args=[book_to_edit.id]), edit_data
        )
        self.assertEqual(response.status_code, 302)
        updated_book = Book.objects.get(ISBN="9780007159208")
        self.assertNotEqual(updated_book.title, "Updated Book Title")

    def test_edit_view__developer_cannot_edit_book(self):
        self.client.login(username="developer", password="password")
        book_to_edit = Book.objects.get(title=self.book2.title)
        author = Author.objects.get(id=book_to_edit.author.id)
        edit_data = {
            "title": "Updated Book Title",
            "author": author.id,
            "publication_year": 1985,
            "ISBN": "9780007159208",
            "image": "http://books.google.com/books/content?id=1YP-hfna5ewC&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        }

        response = self.client.post(
            reverse("books_edit", args=[book_to_edit.id]), edit_data
        )
        self.assertEqual(response.status_code, 302)
        updated_book = Book.objects.get(ISBN="9780007159208")
        self.assertNotEqual(updated_book.title, "Updated Book Title")

    # CHECKOUT BOOK view
    def test_checkout_book_view__customer_can_checkout_book(self):
        self.client.login(username="customer", password="password")
        book_to_checkout = Book.objects.get(title=self.book2.title)

        response = self.client.post(
            reverse("books_checkout", args=[book_to_checkout.id])
        )
        self.assertEqual(response.status_code, 302)
        bookLoan = BookLoan.objects.get(user=self.customer_user)
        book_to_checkout_id = Book.objects.get(title=self.book2.title).id
        self.assertEqual(bookLoan.book.id, book_to_checkout_id)

    def test_checkout_book_view__librarian_cannot_checkout_book(self):
        self.client.login(username="librarian", password="password")
        book_to_checkout = Book.objects.get(title=self.book2.title)

        response = self.client.post(
            reverse("books_checkout", args=[book_to_checkout.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BookLoan.objects.filter(user=self.librarian_user).exists())

    def test_checkout_book_view__developer_cannot_checkout_book(self):
        self.client.login(username="developer", password="password")
        book_to_checkout = Book.objects.get(title=self.book2.title)

        response = self.client.post(
            reverse("books_checkout", args=[book_to_checkout.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BookLoan.objects.filter(user=self.developer_user).exists())

    # RETURN BOOK View
    def test_return_book_view__customer_can_return_book(self):
        self.client.login(username="customer", password="password")
        # Checkout Book
        book_to_checkout = Book.objects.get(title=self.book2.title)

        response = self.client.post(
            reverse("books_checkout", args=[book_to_checkout.id])
        )

        # Return Book
        book_to_return = Book.objects.get(title=self.book2.title)
        response = self.client.post(reverse("books_return", args=[book_to_return.id]))
        self.assertEqual(response.status_code, 302)
        bookLoan = BookLoan.objects.get(user=self.customer_user)
        self.assertTrue(bookLoan.returned)

    def test_return_book_view__librarian_cannot_return_book(self):
        self.client.login(username="customer", password="password")
        # Checkout Book
        book_to_checkout = Book.objects.get(title=self.book2.title)

        response = self.client.post(
            reverse("books_checkout", args=[book_to_checkout.id])
        )
        self.client.logout()
        self.client.login(username="librarian", password="password")

        # Return Book
        book_to_return = Book.objects.get(title=self.book2.title)
        response = self.client.post(reverse("books_return", args=[book_to_return.id]))
        self.assertEqual(response.status_code, 302)
        bookLoan = BookLoan.objects.get(user=self.customer_user)
        self.assertFalse(bookLoan.returned)

    def test_return_book_view__developer_cannot_return_book(self):
        self.client.login(username="customer", password="password")
        # Checkout Book
        book_to_checkout = Book.objects.get(title=self.book2.title)

        response = self.client.post(
            reverse("books_checkout", args=[book_to_checkout.id])
        )
        self.client.logout()
        self.client.login(username="developer", password="password")

        # Return Book
        book_to_return = Book.objects.get(title=self.book2.title)
        response = self.client.post(reverse("books_return", args=[book_to_return.id]))
        self.assertEqual(response.status_code, 302)
        bookLoan = BookLoan.objects.get(user=self.customer_user)
        self.assertFalse(bookLoan.returned)
