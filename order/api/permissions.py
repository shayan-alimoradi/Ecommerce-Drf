from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "You must be the owner of this Order"

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user == obj.user)


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
