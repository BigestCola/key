# user/permissions.py

from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == User.TYPE_ADMIN

class IsAgent(BasePermission):  
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in [User.TYPE_AGENT1, User.TYPE_AGENT2]

class IsSuperior(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj in request.user.subordinates.all()