from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects, but allow read-only for others.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to edit their own profiles or allow admins to edit any profile.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow if the user is the owner of the object or an admin
        return obj.user == request.user or request.user.is_staff