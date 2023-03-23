from rest_framework import permissions
from users.models import User


class AuthorAndStaffOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        '''Аутентификация создателя объекта'''
        if request.method in permissions.SAFE_METHODS:
            return True
        return ((request.user == obj.author) or request.user.is_superuser
                or (request.user.role != User.Role.USER))


class IsAdminOrSuperUser(permissions.BasePermission):
    message = (
        'Получить username может только Админ или суперюзер.'
    )

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == User.Role.ADMIN))


class AdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (request.user.role == User.Role.ADMIN)
        )
