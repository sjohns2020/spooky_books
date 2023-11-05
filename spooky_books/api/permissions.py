from rest_framework.permissions import BasePermission


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "profile") and request.user.profile.is_librarian


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "profile") and request.user.profile.is_customer


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "profile") and request.user.profile.is_developer


# Refactored to optimise performance, so the Db is not being
# filtered each time a permission is being checked.
# class IsDeveloper(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name="Developer").exists()
