
from rest_framework import permissions


class Is1CUser(permissions.BasePermission):
    def has_permission(self, request, view):
        """Permission для пользователей группы 1С"""
        return request.user.groups.filter(name='1C_Group').exists()
