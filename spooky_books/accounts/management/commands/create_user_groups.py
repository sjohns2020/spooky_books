from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from accounts.models import User  # Import your custom User model


# Run this file with 'python3 manage.py create_user_groups
class Command(BaseCommand):
    help = "Create user groups with specified permissions"

    def handle(self, *args, **options):
        # Create user groups

        # Customers Can only see books and checkout a book
        customer_group, created = Group.objects.get_or_create(name="Customer")
        # Librarians can perform CRUD on books and Authors
        librarian_group, created = Group.objects.get_or_create(name="Librarian")
        # Developers cant see books
        developer_group, created = Group.objects.get_or_create(name="Developer")

        # Assign permissions to user groups
        customer_permissions = Permission.objects.filter(
            codename__startswith="customers_", content_type__app_label="accounts"
        )
        librarian_permissions = Permission.objects.filter(
            codename__startswith="librarians_", content_type__app_label="accounts"
        )

        # Filter permissions for the "Developer" group containing "can_"
        developer_permissions = Permission.objects.filter(
            codename__contains="can_", content_type__app_label="accounts"
        )

        developer_group.permissions.set(developer_permissions)
        customer_group.permissions.set(customer_permissions)
        librarian_group.permissions.set(librarian_permissions)

        self.stdout.write(
            self.style.SUCCESS("User groups and permissions created successfully")
        )
