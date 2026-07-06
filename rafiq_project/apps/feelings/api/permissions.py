from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated


class IsAuthenticatedWithMessage(BasePermission):
    """
    Allows access only to authenticated users.
    """

    message = "Please sign in to access your feelings."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated(self.message)

        return True