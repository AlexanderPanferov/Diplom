from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Класс для проверки пользователя"""
    def has_object_permission(self, request, view, obj):
        if obj.phone == request.user.phone:
            return True
        return False