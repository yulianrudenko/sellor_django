from rest_framework import permissions

class IsProductOwner(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        if request.method in permissions.SAFE_METHODS or obj is None:
            return True
        return request.user == obj.user
