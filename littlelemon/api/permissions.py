from rest_framework import permissions

class IsManagerOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.groups.filter(name='managers').exists() )
    

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name='managers').exists() )
    
class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Staff can access all orders; users can only access their own
        return request.user.is_staff or obj.user == request.user