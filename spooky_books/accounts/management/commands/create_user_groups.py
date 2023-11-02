from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from accounts.models import User  # Import your custom User model


# Run this file with 'python3 manage.py create_user_groups
class Command(BaseCommand):
    help = "Create user groups with specified permissions"

    def handle(self, *args, **options):
        # Create user groups
        customer_group, created = Group.objects.get_or_create(name="Customer")
        librarian_group, created = Group.objects.get_or_create(name="Librarian")

        # Assign permissions to user groups
        customer_permissions = Permission.objects.filter(
            codename__startswith="customers_", content_type__app_label="accounts"
        )
        librarian_permissions = Permission.objects.filter(
            codename__startswith="librarians_", content_type__app_label="accounts"
        )

        for permission in customer_permissions:
            customer_group.permissions.add(permission)

        for permission in librarian_permissions:
            librarian_group.permissions.add(permission)

        self.stdout.write(
            self.style.SUCCESS("User groups and permissions created successfully")
        )
