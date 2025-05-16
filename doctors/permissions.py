from rest_framework import permissions

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Admins can do anything, doctors can update their own profile or their own availability, others read-only.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True
        # SAFE_METHODS: allow anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Doctors can update their own profile or their own availability
        if request.user.user_type == 'doctor':
            # For DoctorProfile
            if hasattr(obj, 'user') and obj.user == request.user:
                return True
            # For DoctorAvailability
            if hasattr(obj, 'doctor') and hasattr(obj.doctor, 'user') and obj.doctor.user == request.user:
                return True
        return False
