from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User  # Import your custom User model


class Command(BaseCommand):
    help = "Create user groups with specified permissions"

    def handle(self, *args, **options):
        # Define the permissions by group
        customer_permissions_list = [
            ("can_view_books", "Can view books"),
            ("can_view_authors", "Can view authors"),
            # Only a customer can checkout a book
            ("can_checkout_book", "Can checkout book"),
        ]
        librarian_permissions_list = [
            ("can_view_books", "Can view books"),
            ("can_view_authors", "Can view authors"),
            ("can_add_books", "Can add books"),
            ("can_update_books", "Can update books"),
            ("can_delete_books", "Can delete books"),
            ("can_add_authors", "Can add authors"),
            ("can_update_authors", "Can update authors"),
            ("can_delete_authors", "Can delete authors"),
            ("can_view_bookloans", "Can view bookloans"),
            ("can_add_bookloans", "Can add bookloans"),
            ("can_update_bookloans", "Can update bookloans"),
            ("can_delete_bookloans", "Can delete bookloans"),
        ]
        developer_permissions_list = [
            ("can_view_books", "Can view books"),
            ("can_view_authors", "Can view authors"),
            ("can_add_books", "Can add books"),
            ("can_update_books", "Can update books"),
            ("can_delete_books", "Can delete books"),
            ("can_add_authors", "Can add authors"),
            ("can_update_authors", "Can update authors"),
            ("can_delete_authors", "Can delete authors"),
            # Developers do not have permissions for bookloans
        ]

        # Create the groups
        customer_group, _ = Group.objects.get_or_create(name="Customer")
        librarian_group, _ = Group.objects.get_or_create(name="Librarian")
        developer_group, _ = Group.objects.get_or_create(name="Developer")

        # Get the content type for your User model
        user_content_type = ContentType.objects.get_for_model(User)

        # Create permissions if they don't exist and add them to the groups
        for codename, name in customer_permissions_list:
            perm, _ = Permission.objects.get_or_create(
                codename=codename, name=name, content_type=user_content_type
            )
            customer_group.permissions.add(perm)

        for codename, name in librarian_permissions_list:
            perm, _ = Permission.objects.get_or_create(
                codename=codename, name=name, content_type=user_content_type
            )
            librarian_group.permissions.add(perm)

        for codename, name in developer_permissions_list:
            perm, _ = Permission.objects.get_or_create(
                codename=codename, name=name, content_type=user_content_type
            )
            developer_group.permissions.add(perm)

        # Provide output to the console
        self.stdout.write(
            self.style.SUCCESS("User groups and permissions created successfully")
        )
