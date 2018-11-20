from rest_framework.permissions import BasePermission
from articles.models import User


class ArticlePermissions(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated or request.method == 'GET'

    def has_object_permission(self, request, view, obj):

        return request.method == 'GET' or request.user.is_superuser or request.user == obj.owner


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return request.user.id == obj.id


class UserListCreatePermission(BasePermission):

    def has_permission(self, request, view):

        return True

    def has_object_permission(self, request, view, obj):
        return False


class NoPermission(BasePermission):

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class CategoryPermission(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_superuser or request.method == 'GET'

    def has_object_permission(self, request, view, obj):

        return request.user.is_superuser


class HighlightPermission(BasePermission):

    def has_permission(self, request, view):

        return request.user.is_authenticated or request.user.is_superuser or request.method == 'GET' or request.method == 'POST'

    def has_object_permission(self, request, view, obj):

        return request.user.is_superuser or request.user == obj.owner
