from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.group.filter(name='Manager').exists()


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.group.filter(name='Client').exists()

