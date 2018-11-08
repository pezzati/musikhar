from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission


class IsAuthenticatedNotGuest(BasePermission):
    """
    Allows access only to authenticated and verified users.
    """

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user) and not request.user.is_guest
