from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class that allows only admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsStaffOrAdmin(permissions.BasePermission):
    """
    Permission class that allows staff and admin users.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['staff', 'admin']
        )


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Permission class that allows owners to access their own objects,
    or staff/admin to access all objects.
    """
    def has_object_permission(self, request, view, obj):
        # Admin and staff can access everything
        if request.user.role in ['staff', 'admin']:
            return True
        
        # Check if object has customer_id and matches user
        if hasattr(obj, 'customer_id'):
            return obj.customer_id == getattr(request.user, 'customer_id', None)
        
        return False


class ReadOnly(permissions.BasePermission):
    """
    Permission class that allows read-only access for safe methods.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

